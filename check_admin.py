"""
檢查管理員帳號配置
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gradeSystem.settings')
django.setup()

from django.contrib.auth.models import User
from courses.models import UserProfile

def check_admin():
    print("檢查管理員帳號配置...\n")
    
    try:
        admin = User.objects.get(username='admin')
        print(f"[OK] 找到管理員帳號: {admin.username}")
        print(f"  - Email: {admin.email}")
        print(f"  - 姓名: {admin.get_full_name()}")
        print(f"  - is_staff: {admin.is_staff}")
        print(f"  - is_superuser: {admin.is_superuser}")
        
        try:
            profile = admin.profile
            print(f"\n[OK] 找到 UserProfile:")
            print(f"  - Role: {profile.role}")
            print(f"  - Bio: {profile.bio}")
            
            # 檢查登入重定向條件
            print(f"\n檢查登入重定向條件:")
            print(f"  - profile.role == 'admin': {profile.role == 'admin'}")
            print(f"  - is_staff: {admin.is_staff}")
            print(f"  - 應該重定向到: ", end="")
            if profile.role == 'admin':
                print("admin_dashboard [OK]")
            elif profile.role == 'teacher':
                print("teacher_dashboard")
            else:
                print("student_dashboard")
                
        except UserProfile.DoesNotExist:
            print("\n[ERROR] 管理員沒有 UserProfile!")
            print("  正在創建...")
            profile = UserProfile.objects.create(user=admin, role='admin', bio='系統管理員')
            print(f"  [OK] 已創建 UserProfile (role={profile.role})")
            
    except User.DoesNotExist:
        print("[ERROR] 找不到管理員帳號 'admin'")
        print("\n請先執行初始化腳本:")
        print("  python manage.py shell < init_script.py")

if __name__ == '__main__':
    check_admin()
