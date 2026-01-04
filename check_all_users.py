"""
檢查所有用戶的 role 配置
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gradeSystem.settings')
django.setup()

from django.contrib.auth.models import User
from courses.models import UserProfile, Teacher

def check_all_users():
    print("檢查所有用戶帳號...\n")
    
    users = User.objects.all().order_by('-date_joined')[:10]
    
    for user in users:
        print(f"\n{'='*60}")
        print(f"用戶名: {user.username}")
        print(f"Email: {user.email}")
        print(f"註冊時間: {user.date_joined}")
        
        try:
            profile = user.profile
            print(f"[OK] UserProfile 存在:")
            print(f"  - role: {profile.role}")
            
            # 檢查是否應該有 Teacher 對象
            if profile.role == 'teacher':
                try:
                    teacher = Teacher.objects.get(user=user)
                    print(f"[OK] Teacher 對象存在 (teacher_id={teacher.teacher_id})")
                except Teacher.DoesNotExist:
                    print(f"[ERROR] role='teacher' 但沒有 Teacher 對象!")
                    
        except UserProfile.DoesNotExist:
            print(f"[ERROR] 沒有 UserProfile!")

if __name__ == '__main__':
    check_all_users()
