"""
檢查最近創建的教師帳號
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gradeSystem.settings')
django.setup()

from django.contrib.auth.models import User
from courses.models import UserProfile, Teacher

def check_recent_teachers():
    print("檢查最近創建的教師帳號...\n")
    
    # 獲取所有教師 profile
    teacher_profiles = UserProfile.objects.filter(role='teacher').order_by('-created_at')[:5]
    
    if not teacher_profiles:
        print("[INFO] 沒有找到教師帳號")
        return
    
    for profile in teacher_profiles:
        user = profile.user
        print(f"\n{'='*60}")
        print(f"用戶名: {user.username}")
        print(f"Email: {user.email}")
        print(f"姓名: {user.get_full_name()} (first_name='{user.first_name}', last_name='{user.last_name}')")
        print(f"UserProfile.role: {profile.role}")
        print(f"創建時間: {profile.created_at}")
        
        # 檢查是否有對應的 Teacher 對象
        try:
            teacher = Teacher.objects.get(user=user)
            print(f"[OK] Teacher 對象存在:")
            print(f"  - teacher_id: {teacher.teacher_id}")
            print(f"  - department: {teacher.department}")
        except Teacher.DoesNotExist:
            print(f"[ERROR] 沒有對應的 Teacher 對象!")
        
        # 檢查登入重定向
        print(f"\n登入重定向檢查:")
        print(f"  - profile.role == 'teacher': {profile.role == 'teacher'}")
        if profile.role == 'teacher':
            print(f"  - 應該重定向到: teacher_dashboard [OK]")
        else:
            print(f"  - 應該重定向到: {profile.role}_dashboard [ERROR]")

if __name__ == '__main__':
    check_recent_teachers()
