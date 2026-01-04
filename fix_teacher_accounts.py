"""
修復被錯誤創建為學生的教師帳號
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gradeSystem.settings')
django.setup()

from django.contrib.auth.models import User
from courses.models import UserProfile, Teacher

def fix_teacher_accounts():
    print("檢查並修復教師帳號...\n")
    
    # 查找可能是教師但被標記為學生的帳號
    # 這些帳號通常 email 為空或者用戶名看起來像教師編號
    suspicious_users = User.objects.filter(
        profile__role='student',
        email=''
    ).order_by('-date_joined')[:5]
    
    if not suspicious_users:
        print("[INFO] 沒有找到可疑的帳號")
        return
    
    print(f"找到 {suspicious_users.count()} 個可疑帳號:\n")
    
    for user in suspicious_users:
        print(f"{'='*60}")
        print(f"用戶名: {user.username}")
        print(f"Email: {user.email or '(空)'}")
        print(f"註冊時間: {user.date_joined}")
        print(f"當前 role: {user.profile.role}")
        
        # 詢問是否要轉換為教師
        response = input(f"\n是否要將此帳號轉換為教師? (y/n): ").strip().lower()
        
        if response == 'y':
            # 獲取教師信息
            teacher_id = input("請輸入教工編號: ").strip()
            department = input("請輸入所屬部門 (可選): ").strip()
            
            # 更新 profile
            profile = user.profile
            profile.role = 'teacher'
            profile.save()
            
            # 創建 Teacher 對象
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
                teacher.teacher_id = teacher_id
                teacher.department = department
                teacher.save()
                print(f"[OK] 已更新 Teacher 對象")
            
            print(f"[OK] 帳號 {user.username} 已轉換為教師")
        else:
            print("[SKIP] 跳過此帳號")
        
        print()

if __name__ == '__main__':
    fix_teacher_accounts()
