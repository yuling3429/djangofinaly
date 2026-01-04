from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.http import require_http_methods
from django.db.models import Q, Avg
from .models import Student, Course, Enrollment, Teacher, UserProfile, CourseComment
from .forms import (
    UserRegistrationForm, UserProfileForm, UserEditForm, 
    TeacherForm, CourseForm, TeacherCourseForm, EnrollmentForm, CourseCommentForm
)


# 首頁視圖
def index(request):
    """系統首頁"""
    context = {
        'title': '成績系統',
        'page': 'index'
    }
    return render(request, 'courses/index.html', context)


# 用戶認證視圖
def register(request):
    """用戶註冊"""
    if request.user.is_authenticated:
        # 根據角色重定向到相應的儀表板
        try:
            profile = request.user.profile
            if profile.role == 'teacher':
                return redirect('courses:teacher_dashboard')
            elif profile.role == 'admin':
                return redirect('courses:admin_dashboard')
            else:
                return redirect('courses:student_dashboard')
        except UserProfile.DoesNotExist:
            return redirect('courses:complete_profile')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # 創建用戶資料
            UserProfile.objects.create(user=user, role='student')
            login(request, user)
            return redirect('courses:complete_profile')
    else:
        form = UserRegistrationForm()
    
    context = {
        'form': form,
        'title': '註冊帳號',
        'page': 'register'
    }
    return render(request, 'courses/register.html', context)


def user_login(request):
    """用戶登入"""
    if request.user.is_authenticated:
        # 根據角色重定向到相應的儀表板
        try:
            profile = request.user.profile
            if profile.role == 'teacher':
                return redirect('courses:teacher_dashboard')
            elif profile.role == 'admin':
                return redirect('courses:admin_dashboard')
            else:
                return redirect('courses:student_dashboard')
        except UserProfile.DoesNotExist:
            return redirect('courses:complete_profile')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            # 根據角色重定向到相應的儀表板
            try:
                profile = user.profile
                if profile.role == 'teacher':
                    return redirect('courses:teacher_dashboard')
                elif profile.role == 'admin':
                    return redirect('courses:admin_dashboard')
                else:
                    return redirect('courses:student_dashboard')
            except UserProfile.DoesNotExist:
                # 不要自動創建 profile,而是顯示錯誤訊息
                logout(request)
                context = {
                    'error': '您的帳號尚未完成設定,請聯繫管理員',
                    'title': '登入'
                }
                return render(request, 'courses/login.html', context)
        else:
            context = {'error': '用戶名或密碼不正確', 'title': '登入'}
            return render(request, 'courses/login.html', context)
    
    context = {'title': '登入', 'page': 'login'}
    return render(request, 'courses/login.html', context)


def user_logout(request):
    """用戶登出"""
    logout(request)
    return redirect('courses:index')


@login_required
def complete_profile(request):
    """完善用戶資料"""
    profile = request.user.profile
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            if profile.role == 'student':
                return redirect('courses:student_dashboard')
            elif profile.role == 'teacher':
                return redirect('courses:teacher_dashboard')
            else:
                return redirect('courses:admin_dashboard')
    else:
        form = UserProfileForm(instance=profile)
    
    context = {
        'form': form,
        'profile': profile,
        'title': '完善資料',
        'page': 'complete_profile'
    }
    return render(request, 'courses/complete_profile.html', context)


@login_required
def profile(request):
    """用戶資料頁面"""
    profile = request.user.profile
    
    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            context = {
                'user_form': user_form,
                'profile_form': profile_form,
                'profile': profile,
                'title': '個人資料',
                'success': '資料已更新！'
            }
            return render(request, 'courses/profile.html', context)
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = UserProfileForm(instance=profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'profile': profile,
        'title': '個人資料',
        'page': 'profile'
    }
    return render(request, 'courses/profile.html', context)


# 學生視圖
@login_required
def student_dashboard(request):
    """學生成績單"""
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        return HttpResponseForbidden('您的帳號尚未完成設定,請聯繫管理員')
    
    if profile.role != 'student':
        return HttpResponseForbidden('只有學生可以訪問此頁面')
    
    user = request.user
    enrollments = Enrollment.objects.filter(user=user, is_active=True)
    
    # 計算平均分數
    total_scores = []
    for enrollment in enrollments:
        score = enrollment.get_total_score()
        if score is not None:
            total_scores.append(score)
    
    average_score = sum(total_scores) / len(total_scores) if total_scores else 0
    average_score = round(average_score, 2)
    
    context = {
        'user': user,
        'enrollments': enrollments,
        'average_score': average_score,
        'page': 'student_dashboard',
        'title': f'{user.get_full_name()}的成績單'
    }
    return render(request, 'courses/student_dashboard.html', context)


# 課程視圖
def course_list(request):
    """課程列表"""
    courses = Course.objects.all()
    search = request.GET.get('search', '')
    
    if search:
        courses = courses.filter(
            Q(course_code__icontains=search) | 
            Q(course_name__icontains=search) |
            Q(teacher__user__first_name__icontains=search)
        )
    
    context = {
        'courses': courses,
        'search': search,
        'page': 'course_list',
        'title': '課程列表'
    }
    return render(request, 'courses/course_list.html', context)


def course_detail(request, course_id):
    """課程詳細信息和留言"""
    course = get_object_or_404(Course, pk=course_id)
    enrollments = Enrollment.objects.filter(course=course, is_active=True)
    comments = CourseComment.objects.filter(course=course)
    
    can_comment = False
    user_comment = None
    
    if request.user.is_authenticated:
        # 檢查用戶是否選修了該課程
        user_enrollment = enrollments.filter(user=request.user).exists()
        if user_enrollment:
            can_comment = True
        
        # 獲取用戶自己的留言
        user_comment = comments.filter(user=request.user).first()
    
    # 處理留言提交
    if request.method == 'POST' and request.user.is_authenticated and can_comment:
        comment_id = request.POST.get('comment_id')
        content = request.POST.get('content')
        
        if comment_id:
            # 編輯現有留言
            comment = get_object_or_404(CourseComment, id=comment_id, user=request.user)
            comment.content = content
            comment.save()
        else:
            # 創建新留言
            CourseComment.objects.create(
                course=course,
                user=request.user,
                content=content
            )
        
        return redirect('courses:course_detail', course_id=course.pk)
    
    context = {
        'course': course,
        'enrollments': enrollments,
        'comments': comments,
        'can_comment': can_comment,
        'user_comment': user_comment,
        'page': 'course_detail',
        'title': f'{course.course_name} - 課程詳情'
    }
    return render(request, 'courses/course_detail.html', context)


@login_required
def add_enrollment(request, course_id):
    """學生選課"""
    if request.user.profile.role != 'student':
        return HttpResponseForbidden('只有學生可以選課')
    
    course = get_object_or_404(Course, pk=course_id)
    user = request.user
    
    # 檢查是否已選修
    existing = Enrollment.objects.filter(user=user, course=course).first()
    
    if existing:
        if not existing.is_active:
            existing.is_active = True
            existing.save()
    else:
        if course.get_current_enrollment_count() < course.max_students:
            Enrollment.objects.create(user=user, course=course)
    
    return redirect('courses:student_dashboard')


@login_required
def drop_course(request, enrollment_id):
    """學生退選課程"""
    enrollment = get_object_or_404(Enrollment, pk=enrollment_id)
    
    if enrollment.user != request.user:
        return HttpResponseForbidden('無法退選他人的課程')
    
    enrollment.is_active = False
    enrollment.save()
    
    return redirect('courses:student_dashboard')


# 教師視圖
@login_required
def teacher_dashboard(request):
    """教師儀表板"""
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        return HttpResponseForbidden('您的帳號沒有關聯的用戶資料，請聯繫管理員')
    
    if profile.role != 'teacher':
        return HttpResponseForbidden('只有教師可以訪問此頁面')
    
    try:
        teacher = Teacher.objects.get(user=request.user)
    except Teacher.DoesNotExist:
        return redirect('courses:complete_profile')
    
    courses = teacher.get_courses()
    
    context = {
        'teacher': teacher,
        'courses': courses,
        'page': 'teacher_dashboard',
        'title': f'{request.user.get_full_name()}的教師儀表板'
    }
    return render(request, 'courses/teacher_dashboard.html', context)


@login_required
def teacher_add_course(request):
    """教師新增課程"""
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        return HttpResponseForbidden('您的帳號沒有關聯的用戶資料,請聯繫管理員')
    
    if profile.role != 'teacher':
        return HttpResponseForbidden('只有教師可以新增課程')
    
    try:
        teacher = Teacher.objects.get(user=request.user)
    except Teacher.DoesNotExist:
        return HttpResponseForbidden('您的教師資料不完整,請聯繫管理員')
    
    if request.method == 'POST':
        form = TeacherCourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.teacher = teacher
            course.save()
            
            from django.contrib import messages
            messages.success(request, f'課程 {course.course_name} 已成功建立!')
            return redirect('courses:teacher_dashboard')
    else:
        form = TeacherCourseForm()
    
    context = {
        'form': form,
        'title': '新增課程',
        'page': 'teacher_add_course'
    }
    return render(request, 'courses/teacher_add_course.html', context)


@login_required
def teacher_course_students(request, course_id):
    """查看教師的課程選修學生"""
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        return HttpResponseForbidden('您的帳號沒有關聯的用戶資料,請聯繫管理員')
    
    course = get_object_or_404(Course, pk=course_id)
    
    if profile.role != 'teacher' or course.teacher.user != request.user:
        return HttpResponseForbidden('無法訪問其他教師的課程')
    
    enrollments = Enrollment.objects.filter(course=course, is_active=True)
    
    # 處理成績更新
    if request.method == 'POST':
        enrollment_id = request.POST.get('enrollment_id')
        midterm = request.POST.get('midterm_score')
        final = request.POST.get('final_score')
        
        enrollment = get_object_or_404(Enrollment, id=enrollment_id, course=course)
        updated = False
        if midterm:
            enrollment.midterm_score = midterm
            updated = True
        if final:
            enrollment.final_score = final
            updated = True
        
        if updated:
            enrollment.save()
            from django.contrib import messages
            messages.success(request, f'已成功更新 {enrollment.user.get_full_name()} 的成績!')
        
        return redirect('courses:teacher_course_students', course_id=course.pk)
    
    context = {
        'course': course,
        'enrollments': enrollments,
        'page': 'teacher_course_students',
        'title': f'{course.course_name} - 修課學生'
    }
    return render(request, 'courses/teacher_course_students.html', context)


# 管理員視圖
@login_required
def admin_dashboard(request):
    """管理員儀表板"""
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        return HttpResponseForbidden('您的帳號沒有關聯的用戶資料，請聯繫管理員')
    
    if not request.user.is_staff or profile.role != 'admin':
        return HttpResponseForbidden('只有管理員可以訪問此頁面')
    
    stats = {
        'total_users': User.objects.count(),
        'total_students': UserProfile.objects.filter(role='student').count(),
        'total_teachers': UserProfile.objects.filter(role='teacher').count(),
        'total_courses': Course.objects.count(),
        'total_enrollments': Enrollment.objects.filter(is_active=True).count(),
    }
    
    context = {
        'stats': stats,
        'page': 'admin_dashboard',
        'title': '管理員儀表板'
    }
    return render(request, 'courses/admin_dashboard.html', context)


@login_required
def admin_add_teacher(request):
    """管理員新增教師帳號"""
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        return HttpResponseForbidden('您的帳號沒有關聯的用戶資料,請聯繫管理員')
    
    if not request.user.is_staff or profile.role != 'admin':
        return HttpResponseForbidden('只有管理員可以執行此操作')
    
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        teacher_form = TeacherForm(request.POST)
        
        if user_form.is_valid() and teacher_form.is_valid():
            # 創建用戶
            user = user_form.save()
            
            # 從 teacher_form 獲取 first_name 和 last_name (如果有的話)
            if 'first_name' in teacher_form.cleaned_data:
                user.first_name = teacher_form.cleaned_data['first_name']
            if 'last_name' in teacher_form.cleaned_data:
                user.last_name = teacher_form.cleaned_data['last_name']
            user.save()
            
            # 創建教師 profile
            profile = UserProfile.objects.create(user=user, role='teacher')
            
            # 創建 Teacher 對象
            teacher = teacher_form.save(commit=False)
            teacher.user = user
            teacher.save()
            
            # 重定向到教師列表頁面,顯示成功訊息
            from django.contrib import messages
            messages.success(request, f'教師帳號 {user.username} 已成功建立!')
            return redirect('courses:admin_teacher_list')
    else:
        user_form = UserRegistrationForm()
        teacher_form = TeacherForm()
    
    context = {
        'user_form': user_form,
        'teacher_form': teacher_form,
        'title': '新增教師帳號',
        'page': 'admin_add_teacher'
    }
    return render(request, 'courses/admin_add_teacher.html', context)


@login_required
def admin_add_course(request):
    """管理員新增課程"""
    if not request.user.is_staff or request.user.profile.role != 'admin':
        return HttpResponseForbidden('只有管理員可以執行此操作')
    
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            context = {
                'form': form,
                'success': '課程已建立！',
                'title': '新增課程'
            }
            return render(request, 'courses/admin_add_course.html', context)
    else:
        form = CourseForm()
    
    context = {
        'form': form,
        'title': '新增課程',
        'page': 'admin_add_course'
    }
    return render(request, 'courses/admin_add_course.html', context)


@login_required
def admin_teacher_list(request):
    """管理員查看教師列表"""
    if not request.user.is_staff or request.user.profile.role != 'admin':
        return HttpResponseForbidden('只有管理員可以執行此操作')
    
    teachers = Teacher.objects.all()
    
    context = {
        'teachers': teachers,
        'title': '教師管理',
        'page': 'admin_teacher_list'
    }
    return render(request, 'courses/admin_teacher_list.html', context)


@login_required
def admin_delete_teacher(request, teacher_id):
    """管理員刪除教師"""
    if not request.user.is_staff or request.user.profile.role != 'admin':
        return HttpResponseForbidden('只有管理員可以執行此操作')
    
    teacher = get_object_or_404(Teacher, pk=teacher_id)
    user = teacher.user
    
    if request.method == 'POST':
        # 刪除關聯的 User 會級聯刪除 Teacher 和 UserProfile
        user.delete()
        return redirect('courses:admin_teacher_list')
    
    context = {
        'object': teacher,
        'type': '教師',
        'title': '確認刪除'
    }
    return render(request, 'courses/confirm_delete.html', context)


@login_required
def admin_course_list(request):
    """管理員查看課程列表"""
    if not request.user.is_staff or request.user.profile.role != 'admin':
        return HttpResponseForbidden('只有管理員可以執行此操作')
    
    courses = Course.objects.all()
    
    context = {
        'courses': courses,
        'title': '課程管理',
        'page': 'admin_course_list'
    }
    return render(request, 'courses/admin_course_list.html', context)


@login_required
def admin_delete_course(request, course_id):
    """管理員刪除課程"""
    if not request.user.is_staff or request.user.profile.role != 'admin':
        return HttpResponseForbidden('只有管理員可以執行此操作')
    
    course = get_object_or_404(Course, pk=course_id)
    
    if request.method == 'POST':
        course.delete()
        return redirect('courses:admin_course_list')
    
    context = {
        'object': course,
        'type': '課程',
        'title': '確認刪除'
    }
    return render(request, 'courses/confirm_delete.html', context)
