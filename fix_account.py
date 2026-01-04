"""
修復特定教師帳號
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gradeSystem.settings')
django.setup()

from django.contrib.auth.models import User
from courses.models import UserProfile, Teacher

def fix_account(username, teacher_id, department=''):
    print(f"修復帳號: {username}\n")
    
    try:
        user = User.objects.get(username=username)
        print(f"[OK] 找到用戶: {user.username}")
        
        # 更新或創建 UserProfile
        profile, created = UserProfile.objects.get_or_create(user=user)
        if profile.role != 'teacher':
            print(f"  - 將 role 從 '{profile.role}' 改為 'teacher'")
            profile.role = 'teacher'
            profile.save()
        else:
            print(f"  - role 已經是 'teacher'")
        
        # 創建或更新 Teacher 對象
        teacher, created = Teacher.objects.get_or_create(
            user=user,
            defaults={
                'teacher_id': teacher_id,
                'department': department
            }
        )
        
        if created:
            print(f"[OK] 已創建 Teacher 對象 (teacher_id={teacher_id})")
        else:
            print(f"[OK] Teacher 對象已存在 (teacher_id={teacher.teacher_id})")
        
        print(f"\n[SUCCESS] 帳號 {username} 已修復為教師帳號!")
        print(f"  - UserProfile.role: {profile.role}")
        print(f"  - Teacher.teacher_id: {teacher.teacher_id}")
        print(f"  - Teacher.department: {teacher.department}")
        
    except User.DoesNotExist:
        print(f"[ERROR] 找不到用戶: {username}")

if __name__ == '__main__':
    # 修復 11256000 帳號
    # 請根據實際情況修改 teacher_id 和 department
    fix_account('11256000', 'T999', '測試部門')
