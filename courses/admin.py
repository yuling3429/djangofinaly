from django.contrib import admin
from .models import Student, Course, Enrollment, Teacher, UserProfile, CourseComment


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'student_id', 'teacher_id', 'created_at')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'student_id', 'teacher_id')
    list_filter = ('role', 'created_at')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('teacher_id', 'get_full_name', 'department', 'created_at')
    search_fields = ('teacher_id', 'user__first_name', 'user__last_name')
    list_filter = ('department', 'created_at')
    readonly_fields = ('created_at',)

    def get_full_name(self, obj):
        return obj.user.get_full_name()
    get_full_name.short_description = '姓名'


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'name', 'email', 'created_at')
    search_fields = ('student_id', 'name', 'email')
    list_filter = ('created_at',)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_code', 'course_name', 'teacher', 'credits', 'get_current_enrollment_count', 'semester')
    search_fields = ('course_code', 'course_name', 'teacher__user__first_name')
    list_filter = ('credits', 'semester', 'created_at')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('get_user_name', 'course', 'midterm_score', 'final_score', 'is_active')
    search_fields = ('user__first_name', 'user__last_name', 'course__course_name')
    list_filter = ('is_active', 'course', 'enrolled_at')
    list_editable = ('midterm_score', 'final_score', 'is_active')
    readonly_fields = ('enrolled_at', 'updated_at')

    def get_user_name(self, obj):
        return obj.user.get_full_name() or obj.user.username
    get_user_name.short_description = '學生'


@admin.register(CourseComment)
class CourseCommentAdmin(admin.ModelAdmin):
    list_display = ('get_user_name', 'course', 'get_short_content', 'created_at')
    search_fields = ('user__first_name', 'user__last_name', 'course__course_name', 'content')
    list_filter = ('course', 'created_at')
    readonly_fields = ('created_at', 'updated_at')

    def get_user_name(self, obj):
        return obj.user.get_full_name() or obj.user.username
    get_user_name.short_description = '留言者'

    def get_short_content(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    get_short_content.short_description = '留言內容'
