from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Course, Enrollment, Student, Teacher, UserProfile, CourseComment


# 用戶認證表單
class UserRegistrationForm(UserCreationForm):
    """用戶註冊表單"""
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '用戶名'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '名字'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '姓氏'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '電子郵件'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': '密碼'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': '確認密碼'})


# 用戶資料表單
class UserProfileForm(forms.ModelForm):
    """用戶資料表單"""
    class Meta:
        model = UserProfile
        fields = ['avatar', 'bio', 'phone']
        widgets = {
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'placeholder': '個人簡介', 'rows': 4}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '電話'}),
        }


# 用戶信息編輯表單
class UserEditForm(UserChangeForm):
    """編輯用戶信息表單"""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '名字'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '姓氏'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '電子郵件'}),
        }


# 教師表單
class TeacherForm(forms.ModelForm):
    """教師表單"""
    first_name = forms.CharField(max_length=100, required=True, label='名字')
    last_name = forms.CharField(max_length=100, required=False, label='姓氏')
    
    class Meta:
        model = Teacher
        fields = ['teacher_id', 'department', 'bio']
        widgets = {
            'teacher_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '教工編號'}),
            'department': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '所屬部門'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'placeholder': '教師簡介', 'rows': 4}),
        }




# 課程表單
class CourseForm(forms.ModelForm):
    """課程表單"""
    class Meta:
        model = Course
        fields = ['course_code', 'course_name', 'teacher', 'credits', 'description', 'max_students', 'semester']
        widgets = {
            'course_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '課號'}),
            'course_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '課名'}),
            'teacher': forms.Select(attrs={'class': 'form-control'}),
            'credits': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '學分'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': '課程描述', 'rows': 4}),
            'max_students': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '最大選修人數'}),
            'semester': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '學期（如：2024-1）'}),
        }


class TeacherCourseForm(forms.ModelForm):
    """教師新增課程表單(不包含教師選擇)"""
    class Meta:
        model = Course
        fields = ['course_code', 'course_name', 'credits', 'description', 'max_students', 'semester']
        widgets = {
            'course_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '課號'}),
            'course_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '課名'}),
            'credits': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '學分', 'value': 3}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': '課程描述', 'rows': 4}),
            'max_students': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '最大選修人數', 'value': 50}),
            'semester': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '學期（如：2025-1）'}),
        }



# 成績表單
class EnrollmentForm(forms.ModelForm):
    """選課表單"""
    class Meta:
        model = Enrollment
        fields = ['midterm_score', 'final_score']
        widgets = {
            'midterm_score': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '期中分數', 'step': '0.01', 'min': '0', 'max': '100'}),
            'final_score': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '期末分數', 'step': '0.01', 'min': '0', 'max': '100'}),
        }


# 課程留言表單
class CourseCommentForm(forms.ModelForm):
    """課程留言表單"""
    class Meta:
        model = CourseComment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': '輸入你的留言...', 'rows': 3}),
        }


# 學生表單（向後相容）
class StudentForm(forms.ModelForm):
    """學生表單"""
    class Meta:
        model = Student
        fields = ['student_id', 'name', 'email']
        widgets = {
            'student_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '學號'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '姓名'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '信箱'}),
        }
