"""
檢查特定用戶帳號
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gradeSystem.settings')
django.setup()

from django.contrib.auth.models import User
from courses.models import UserProfile, Teacher

def check_user(username):
    print(f"檢查用戶: {username}\n")
    
    try:
        user = User.objects.get(username=username)
        print(f"[OK] 找到用戶: {user.username}")
        print(f"  - Email: {user.email or '(空)'}")
        print(f"  - 姓名: {user.get_full_name()} (first='{user.first_name}', last='{user.last_name}')")
        print(f"  - 註冊時間: {user.date_joined}")
        
        try:
            profile = user.profile
            print(f"\n[OK] UserProfile 存在:")
            print(f"  - role: {profile.role}")
            print(f"  - 創建時間: {profile.created_at}")
            
            # 檢查 Teacher 對象
            try:
                teacher = Teacher.objects.get(user=user)
                print(f"\n[OK] Teacher 對象存在:")
                print(f"  - teacher_id: {teacher.teacher_id}")
                print(f"  - department: {teacher.department}")
            except Teacher.DoesNotExist:
                print(f"\n[ERROR] 沒有 Teacher 對象!")
                print(f"  這就是問題所在 - 帳號有 profile.role='teacher' 但沒有 Teacher 對象")
                
        except UserProfile.DoesNotExist:
            print(f"\n[ERROR] 沒有 UserProfile!")
            
    except User.DoesNotExist:
        print(f"[ERROR] 找不到用戶: {username}")

if __name__ == '__main__':
    check_user('11256000')
