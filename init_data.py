"""
初始化數據腳本
執行此腳本以創建測試學生和課程
在manage.py同級目錄執行: python init_data.py
"""

import os
import django
from django.conf import settings

# 設置Django環境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gradeSystem.settings')
django.setup()

from courses.models import Student, Course, Enrollment

def init_data():
    """初始化測試數據"""
    
    # 清空現有數據（可選）
    print("開始初始化數據...")
    
    # 創建學生
    print("\n建立學生...")
    student, created = Student.objects.get_or_create(
        student_id='2024001',
        defaults={
            'name': '王小明',
            'email': 'wangxiaoming@example.com'
        }
    )
    if created:
        print(f"✓ 創建學生: {student}")
    else:
        print(f"✓ 學生已存在: {student}")
    
    # 創建三門課程
    print("\n建立課程...")
    courses_data = [
        {
            'course_code': 'CS101',
            'course_name': '資料結構與演算法',
            'instructor': '李教授',
            'credits': 3,
            'description': '本課程涵蓋基本數據結構如陣列、鏈表、堆棧、隊列等，以及相關演算法。'
        },
        {
            'course_code': 'CS102',
            'course_name': '資料庫系統',
            'instructor': '王教授',
            'credits': 3,
            'description': '學習資料庫設計、SQL語言、資料庫管理系統等內容。'
        },
        {
            'course_code': 'CS103',
            'course_name': '網頁開發',
            'instructor': '陳教授',
            'credits': 3,
            'description': '前後端網頁開發技術，包括HTML、CSS、JavaScript和Django框架。'
        }
    ]
    
    courses = []
    for course_data in courses_data:
        course, created = Course.objects.get_or_create(
            course_code=course_data['course_code'],
            defaults=course_data
        )
        if created:
            print(f"✓ 創建課程: {course}")
        else:
            print(f"✓ 課程已存在: {course}")
        courses.append(course)
    
    # 為學生添加選課記錄
    print("\n建立選課記錄...")
    
    # 添加模擬成績
    scores = [
        {'midterm_score': 85, 'final_score': 88},
        {'midterm_score': 92, 'final_score': 90},
        {'midterm_score': 78, 'final_score': 82}
    ]
    
    for course, score_data in zip(courses, scores):
        enrollment, created = Enrollment.objects.get_or_create(
            student=student,
            course=course,
            defaults={
                'midterm_score': score_data['midterm_score'],
                'final_score': score_data['final_score'],
                'is_active': True
            }
        )
        if created:
            print(f"✓ 添加選課: {student} 選修 {course}")
            print(f"  期中: {score_data['midterm_score']}, 期末: {score_data['final_score']}")
        else:
            print(f"✓ 選課記錄已存在: {student} 選修 {course}")
    
    print("\n✓ 數據初始化完成！")
    print(f"\n系統現有：")
    print(f"  - 學生數: {Student.objects.count()}")
    print(f"  - 課程數: {Course.objects.count()}")
    print(f"  - 選課記錄數: {Enrollment.objects.count()}")

if __name__ == '__main__':
    init_data()
