from django.contrib import admin
from .models import Student, TeacherProfile, Course, Enrollment, ClassSession, Attendance

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("enrollment_number", "user", "gender", "date_of_birth", "parent_phone")
    list_filter = ("gender",)
    search_fields = ("enrollment_number", "user__first_name", "user__last_name")

@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ("employee_id", "user", "department", "phone")
    list_filter = ("department",)
    search_fields = ("employee_id", "user__username", "user__first_name", "user__last_name")

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "teacher", "start_date", "end_date")
    search_fields = ("code", "name")

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("student", "course", "joined_on")
    search_fields = ("student__enrollment_number", "course__code")

@admin.register(ClassSession)
class ClassSessionAdmin(admin.ModelAdmin):
    list_display = ("course", "topic", "date", "start_time", "end_time", "created_by")
    list_filter = ("course", "date")

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ("session", "student", "status", "marked_by", "marked_at")
    list_filter = ("status", "session__course")
    search_fields = ("student__enrollment_number", "session__course__code")
