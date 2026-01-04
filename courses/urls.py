from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    # 首頁和認證
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('complete-profile/', views.complete_profile, name='complete_profile'),
    path('profile/', views.profile, name='profile'),
    
    # 課程相關
    path('courses/', views.course_list, name='course_list'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    
    # 學生功能
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('dashboard/',views.student_dashboard, name='dashboard'),
    path('course/<int:course_id>/enroll/', views.add_enrollment, name='add_enrollment'),
    path('enrollment/<int:enrollment_id>/drop/', views.drop_course, name='drop_course'),
    
    # 教師功能
    path('teacher/', views.teacher_dashboard, name='teacher_dashboard'),
    path('teacher/add-course/', views.teacher_add_course, name='teacher_add_course'),
    path('teacher/course/<int:course_id>/students/', views.teacher_course_students, name='teacher_course_students'),
    
    # 管理員功能
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/teachers/', views.admin_teacher_list, name='admin_teacher_list'),
    path('admin/teachers/add/', views.admin_add_teacher, name='admin_add_teacher'),
    path('admin/teachers/<int:teacher_id>/delete/', views.admin_delete_teacher, name='admin_delete_teacher'),
    path('admin/courses/', views.admin_course_list, name='admin_course_list'),
    path('admin/courses/add/', views.admin_add_course, name='admin_add_course'),
    path('admin/courses/<int:course_id>/delete/', views.admin_delete_course, name='admin_delete_course'),
]
