"""
數據庫重置腳本
"""
import os
import django
import shutil
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gradeSystem.settings')
django.setup()

# 刪除舊遷移文件
migrations_dir = Path('courses/migrations')
if migrations_dir.exists():
    for file in migrations_dir.glob('*.py'):
        if file.name != '__init__.py':
            file.unlink()
            print(f"刪除: {file}")

# 刪除舊數據庫
db_file = Path('db.sqlite3')
if db_file.exists():
    db_file.unlink()
    print("刪除舊數據庫")

print("完成清理！")
