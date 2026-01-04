#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Django 學生成績管理系統 - 初始化測試數據腳本
初始化包含：管理員、教師、學生、課程、選課記錄和評論
"""

import os
import sys
import django
from datetime import datetime

# 設置Django環境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gradeSystem.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from django.contrib.auth.models import User
from courses.models import UserProfile, Teacher, Course, Enrollment, CourseComment

def create_admin_user():
    """建立管理員帳戶"""
    if User.objects.filter(username='admin').exists():
        print("管理員帳戶已存在")
        admin = User.objects.get(username='admin')
    else:
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123456',
            first_name='系統',
            last_name='管理員'
        )
        print(f"[OK] 已建立管理員帳戶: {admin.username}")
    
    # 確保有 UserProfile
    profile, created = UserProfile.objects.get_or_create(
        user=admin,
        defaults={
            'role': 'admin',
            'bio': '系統管理員',
            'phone': '0900-000-000'
        }
    )
    if created:
        print("[OK] 已建立管理員 UserProfile")
    
    return admin

def create_teachers():
    """建立教師帳戶"""
    teachers_data = [
        {
            'username': 'teacher_wang',
            'email': 'wang@example.com',
            'first_name': '王',
            'last_name': '老師',
            'teacher_id': 'T001',
            'department': '資訊工程系'
        },
        {
            'username': 'teacher_liu',
            'email': 'liu@example.com',
            'first_name': '劉',
            'last_name': '老師',
            'teacher_id': 'T002',
            'department': '電機工程系'
        },
        {
            'username': 'teacher_chen',
            'email': 'chen@example.com',
            'first_name': '陳',
            'last_name': '老師',
            'teacher_id': 'T003',
            'department': '數學系'
        }
    ]
    
    teachers = []
    for data in teachers_data:
        user, created = User.objects.get_or_create(
            username=data['username'],
            defaults={
                'email': data['email'],
                'first_name': data['first_name'],
                'last_name': data['last_name']
            }
        )
        if created:
            user.set_password('teacher123456')
            user.save()
            print(f"[OK] 已建立教師帳戶: {user.username}")
        
        # 建立或更新 UserProfile
        profile, _ = UserProfile.objects.get_or_create(
            user=user,
            defaults={
                'role': 'teacher',
                'bio': f"{data['first_name']}{data['last_name']}的個人簡介",
                'phone': '0900-111-111'
            }
        )
        
        # 建立或更新 Teacher
        teacher, _ = Teacher.objects.get_or_create(
            user=user,
            defaults={
                'teacher_id': data['teacher_id'],
                'department': data['department']
            }
        )
        teachers.append(teacher)
    
    return teachers

def create_students():
    """建立學生帳戶"""
    students_data = [
        {
            'username': 'student_wang',
            'email': 'student_wang@example.com',
            'first_name': '王',
            'last_name': '小明',
        },
        {
            'username': 'student_lin',
            'email': 'student_lin@example.com',
            'first_name': '林',
            'last_name': '小芬',
        },
        {
            'username': 'student_huang',
            'email': 'student_huang@example.com',
            'first_name': '黃',
            'last_name': '小華',
        },
        {
            'username': 'student_chen',
            'email': 'student_chen@example.com',
            'first_name': '陳',
            'last_name': '小剛',
        }
    ]
    
    students = []
    for data in students_data:
        user, created = User.objects.get_or_create(
            username=data['username'],
            defaults={
                'email': data['email'],
                'first_name': data['first_name'],
                'last_name': data['last_name']
            }
        )
        if created:
            user.set_password('student123456')
            user.save()
            print(f"[OK] 已建立學生帳戶: {user.username}")
        
        # 建立或更新 UserProfile
        profile, _ = UserProfile.objects.get_or_create(
            user=user,
            defaults={
                'role': 'student',
                'bio': f"{data['first_name']}{data['last_name']}的個人簡介",
                'phone': '0900-222-222'
            }
        )
        students.append(user)
    
    return students

def create_courses(teachers):
    """建立課程"""
    courses_data = [
        {
            'course_code': 'CS101',
            'course_name': 'Python程式設計',
            'credits': 3,
            'semester': '2025春',
            'description': '學習Python基礎與應用，包括變數、函數、物件導向等',
            'max_students': 30,
            'teacher': teachers[0]  # 王老師
        },
        {
            'course_code': 'CS201',
            'course_name': '資料結構',
            'credits': 3,
            'semester': '2025春',
            'description': '學習陣列、鏈表、堆棧、隊列等基本資料結構',
            'max_students': 25,
            'teacher': teachers[0]  # 王老師
        },
        {
            'course_code': 'EE101',
            'course_name': '電路基礎',
            'credits': 4,
            'semester': '2025春',
            'description': '電阻、電容、電感、歐姆定律等基本電路概念',
            'max_students': 20,
            'teacher': teachers[1]  # 劉老師
        },
        {
            'course_code': 'MATH101',
            'course_name': '高等數學I',
            'credits': 4,
            'semester': '2025春',
            'description': '微積分、極限、連續性等數學基礎',
            'max_students': 35,
            'teacher': teachers[2]  # 陳老師
        }
    ]
    
    courses = []
    for data in courses_data:
        course, created = Course.objects.get_or_create(
            course_code=data['course_code'],
            defaults={
                'course_name': data['course_name'],
                'credits': data['credits'],
                'semester': data['semester'],
                'description': data['description'],
                'max_students': data['max_students'],
                'teacher': data['teacher']
            }
        )
        if created:
            print(f"[OK] 已建立課程: {course.course_name}")
        courses.append(course)
    
    return courses

def create_enrollments(students, courses):
    """建立選課記錄"""
    # 定義選課對應關係
    enrollment_data = [
        (students[0], courses[0], 85, 92),  # 王小明 選 Python 期中:85 期末:92
        (students[0], courses[1], 78, 88),  # 王小明 選 資料結構 期中:78 期末:88
        (students[0], courses[3], 92, 95),  # 王小明 選 高等數學 期中:92 期末:95
        (students[1], courses[0], 88, 90),  # 林小芬 選 Python 期中:88 期末:90
        (students[1], courses[2], 76, 82),  # 林小芬 選 電路基礎 期中:76 期末:82
        (students[1], courses[3], 95, 98),  # 林小芬 選 高等數學 期中:95 期末:98
        (students[2], courses[1], 72, 80),  # 黃小華 選 資料結構 期中:72 期末:80
        (students[2], courses[2], 85, 88),  # 黃小華 選 電路基礎 期中:85 期末:88
        (students[3], courses[0], 90, 93),  # 陳小剛 選 Python 期中:90 期末:93
        (students[3], courses[3], 88, 91),  # 陳小剛 選 高等數學 期中:88 期末:91
    ]
    
    count = 0
    for student, course, midterm, final in enrollment_data:
        enrollment, created = Enrollment.objects.get_or_create(
            user=student,
            course=course,
            defaults={
                'midterm_score': midterm,
                'final_score': final
            }
        )
        if created:
            count += 1
    
    print(f"[OK] 已建立 {count} 個選課記錄")

def create_comments(students, courses):
    """建立課程評論"""
    comments_data = [
        (students[0], courses[0], '很實用的課程，老師講解清楚'),
        (students[0], courses[1], '內容有點難，但收穫很大'),
        (students[1], courses[0], '程式設計很有趣，推薦！'),
        (students[1], courses[2], '電路課程挺有意思的'),
        (students[2], courses[1], '資料結構是基礎，一定要學好'),
        (students[3], courses[0], '通過這個課程學會了Python'),
    ]
    
    count = 0
    for student, course, content in comments_data:
        comment, created = CourseComment.objects.get_or_create(
            user=student,
            course=course,
            defaults={'content': content}
        )
        if created:
            count += 1
    
    print(f"[OK] 已建立 {count} 個課程評論")

def main():
    """主程式"""
    print("=" * 50)
    print("Django 學生成績管理系統 - 初始化測試數據")
    print("=" * 50)
    
    # 建立管理員
    print("\n[1/6] 建立管理員帳戶...")
    create_admin_user()
    
    # 建立教師
    print("\n[2/6] 建立教師帳戶...")
    teachers = create_teachers()
    print(f"共建立 {len(teachers)} 位教師")
    
    # 建立學生
    print("\n[3/6] 建立學生帳戶...")
    students = create_students()
    print(f"共建立 {len(students)} 位學生")
    
    # 建立課程
    print("\n[4/6] 建立課程...")
    courses = create_courses(teachers)
    print(f"共建立 {len(courses)} 門課程")
    
    # 建立選課記錄
    print("\n[5/6] 建立選課記錄...")
    create_enrollments(students, courses)
    
    # 建立評論
    print("\n[6/6] 建立課程評論...")
    create_comments(students, courses)
    
    print("\n" + "=" * 50)
    print("[OK] 初始化完成！")
    print("=" * 50)
    print("\n測試帳戶：")
    print("  管理員: admin / admin123456")
    print("  教師: teacher_wang / teacher123456")
    print("  學生: student_wang / student123456")
    print("\n訪問: http://localhost:8000/")
    print("=" * 50)

if __name__ == '__main__':
    main()
