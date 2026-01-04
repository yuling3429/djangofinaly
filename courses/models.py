from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from PIL import Image
import os


# 用戶資料擴展模型
class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('student', '學生'),
        ('teacher', '教師'),
        ('admin', '管理者'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name="用戶")
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, verbose_name="角色")
    student_id = models.CharField(max_length=20, unique=True, null=True, blank=True, verbose_name="學號")
    teacher_id = models.CharField(max_length=20, unique=True, null=True, blank=True, verbose_name="教工編號")
    avatar = models.ImageField(upload_to='avatars/%Y/%m/%d/', null=True, blank=True, verbose_name="頭像")
    bio = models.TextField(blank=True, verbose_name="個人簡介")
    phone = models.CharField(max_length=20, blank=True, verbose_name="電話")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="建立時間")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新時間")

    class Meta:
        verbose_name = "用戶資料"
        verbose_name_plural = "用戶資料"

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.get_role_display()})"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # 處理頭像縮放
        if self.avatar:
            self._resize_avatar()

    def _resize_avatar(self):
        """將頭像縮放至300x300像素"""
        if self.avatar:
            img = Image.open(self.avatar.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size, Image.Resampling.LANCZOS)
                img.save(self.avatar.path)


# 教師模型
class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher', verbose_name="用戶")
    teacher_id = models.CharField(max_length=20, unique=True, verbose_name="教工編號")
    department = models.CharField(max_length=100, blank=True, verbose_name="所屬部門")
    bio = models.TextField(blank=True, verbose_name="教師簡介")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="建立時間")

    class Meta:
        verbose_name = "教師"
        verbose_name_plural = "教師"
        ordering = ['teacher_id']

    def __str__(self):
        return f"{self.teacher_id} - {self.user.get_full_name()}"

    def get_courses(self):
        """獲取該教師授課的所有課程"""
        return self.course_set.all()


# 課程模型（更新）
class Course(models.Model):
    course_code = models.CharField(max_length=20, unique=True, verbose_name="課號")
    course_name = models.CharField(max_length=100, verbose_name="課名")
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, related_name='course_set', verbose_name="任課教師")
    credits = models.IntegerField(default=3, verbose_name="學分")
    description = models.TextField(blank=True, verbose_name="課程描述")
    max_students = models.IntegerField(default=50, verbose_name="最大選修人數")
    semester = models.CharField(max_length=20, default='2024-1', verbose_name="學期")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="建立時間")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新時間")

    class Meta:
        verbose_name = "課程"
        verbose_name_plural = "課程"
        ordering = ['course_code']

    def __str__(self):
        return f"{self.course_code} - {self.course_name}"

    def get_enrolled_students(self):
        """取得選修此課程的學生列表"""
        return User.objects.filter(profile__role='student', enrollment__course=self, enrollment__is_active=True).distinct()

    def get_current_enrollment_count(self):
        """取得目前選修人數"""
        return self.enrollment_set.filter(is_active=True).count()

    @property
    def instructor_name(self):
        """獲取教師名稱（向後相容）"""
        return self.teacher.user.get_full_name() if self.teacher else "未設定"


# 選課記錄模型
class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollment_set', verbose_name="學生")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="課程")
    midterm_score = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        null=True, 
        blank=True, 
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="期中分數"
    )
    final_score = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        null=True, 
        blank=True, 
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="期末分數"
    )
    is_active = models.BooleanField(default=True, verbose_name="是否選修中")
    enrolled_at = models.DateTimeField(auto_now_add=True, verbose_name="選課時間")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新時間")

    class Meta:
        verbose_name = "選課記錄"
        verbose_name_plural = "選課記錄"
        unique_together = ('user', 'course')
        ordering = ['-enrolled_at']

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.course}"

    def get_total_score(self):
        """計算該科目的總分（期中、期末平均）"""
        if self.midterm_score is None or self.final_score is None:
            return None
        return round((float(self.midterm_score) + float(self.final_score)) / 2, 2)


# 課程留言模型
class CourseComment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='comments', verbose_name="課程")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="留言者")
    content = models.TextField(verbose_name="留言內容")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="建立時間")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新時間")

    class Meta:
        verbose_name = "課程留言"
        verbose_name_plural = "課程留言"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.course.course_code}"


# 保持與舊系統相容的學生模型
class Student(models.Model):
    student_id = models.CharField(max_length=20, unique=True, verbose_name="學號")
    name = models.CharField(max_length=100, verbose_name="姓名")
    email = models.EmailField(verbose_name="信箱")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="建立時間")

    class Meta:
        verbose_name = "學生"
        verbose_name_plural = "學生"
        ordering = ['student_id']

    def __str__(self):
        return f"{self.student_id} - {self.name}"

    def get_average_score(self):
        """計算學生的平均分數"""
        enrollments = self.enrollment_set.all()
        if not enrollments.exists():
            return 0
        total_score = 0
        for enrollment in enrollments:
            score = enrollment.get_total_score()
            if score is not None:
                total_score += score
        return round(total_score / enrollments.count(), 2)
