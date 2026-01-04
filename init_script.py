from django.contrib.auth.models import User
from courses.models import UserProfile, Teacher, Course, Enrollment, CourseComment

def init_data():
    # 建立管理員
    admin, _ = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@example.com',
            'first_name': '系統',
            'last_name': '管理員',
            'is_staff': True,
            'is_superuser': True
        }
    )
    if admin.password == '' or not admin.check_password('admin123456'):
        admin.set_password('admin123456')
        admin.save()

    profile, _ = UserProfile.objects.get_or_create(
        user=admin,
        defaults={'role': 'admin', 'bio': '系統管理員'}
    )

    # 建立教師
    teachers_data = [
        ('teacher_wang', '王', '老師', 'T001', '資訊工程系'),
        ('teacher_liu', '劉', '老師', 'T002', '電機工程系'),
        ('teacher_chen', '陳', '老師', 'T003', '數學系')
    ]

    teachers = []
    for username, fname, lname, tid, dept in teachers_data:
        user, created = User.objects.get_or_create(
            username=username,
            defaults={'first_name': fname, 'last_name': lname, 'email': f'{username}@example.com'}
        )
        if created:
            user.set_password('teacher123456')
            user.save()
        
        profile, _ = UserProfile.objects.get_or_create(
            user=user,
            defaults={'role': 'teacher'}
        )
        
        teacher, _ = Teacher.objects.get_or_create(
            user=user,
            defaults={'teacher_id': tid, 'department': dept}
        )
        teachers.append(teacher)

    # 建立學生
    students_data = [
        ('student_wang', '王', '小明'),
        ('student_lin', '林', '小芬'),
        ('student_huang', '黃', '小華'),
        ('student_chen', '陳', '小剛')
    ]

    students = []
    for username, fname, lname in students_data:
        user, created = User.objects.get_or_create(
            username=username,
            defaults={'first_name': fname, 'last_name': lname, 'email': f'{username}@example.com'}
        )
        if created:
            user.set_password('student123456')
            user.save()
        
        profile, _ = UserProfile.objects.get_or_create(
            user=user,
            defaults={'role': 'student'}
        )
        students.append(user)

    # 建立課程
    courses_data = [
        ('CS101', 'Python程式設計', 3, '2025春', '學習Python基礎', 30, 0),
        ('CS201', '資料結構', 3, '2025春', '學習資料結構', 25, 0),
        ('EE101', '電路基礎', 4, '2025春', '學習電路基礎', 20, 1),
        ('MATH101', '高等數學I', 4, '2025春', '微積分基礎', 35, 2)
    ]

    courses = []
    for code, name, credits, sem, desc, max_s, t_idx in courses_data:
        course, created = Course.objects.get_or_create(
            course_code=code,
            defaults={
                'course_name': name,
                'credits': credits,
                'semester': sem,
                'description': desc,
                'max_students': max_s,
                'teacher': teachers[t_idx]
            }
        )
        courses.append(course)

    # 建立選課
    enrollments = [
        (0, 0, 85, 92), (0, 1, 78, 88), (0, 3, 92, 95),
        (1, 0, 88, 90), (1, 2, 76, 82), (1, 3, 95, 98),
        (2, 1, 72, 80), (2, 2, 85, 88),
        (3, 0, 90, 93), (3, 3, 88, 91)
    ]

    count = 0
    for s_idx, c_idx, mid, final in enrollments:
        e, created = Enrollment.objects.get_or_create(
            user=students[s_idx],
            course=courses[c_idx],
            defaults={'midterm_score': mid, 'final_score': final}
        )
        if created:
            count += 1

    print("完成！")
    print("管理員: admin / admin123456")
    print("教師: teacher_wang / teacher123456")
    print("學生: student_wang / student123456")

if __name__ == '__main__':
    init_data()
