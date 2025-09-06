from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (
    home,
    StudentRegisterView,
    teacher_register,
    student_login,
    teacher_login,
    admin_login,
    student_dashboard,
    teacher_dashboard,
    manage_courses,
    class_sessions,
    teacher_assignments,
    teacher_schedule,
    teacher_profile,
    admin_dashboard,
)
from .views import student_views   # 👈 add this
from tracker.views import teacher_views


urlpatterns = [
    path("", home, name="home"),

    # Registration
    path("student/register/", StudentRegisterView.as_view(), name="student_register"),
    path("teacher/register/", teacher_register, name="teacher_register"),

    # Login
    path("student/login/", student_login, name="student_login"),
    path("teacher/login/", teacher_login, name="teacher_login"),
    path("admin/login/", admin_login, name="admin_login"),

    # Logout
    path("logout/", LogoutView.as_view(next_page="home"), name="logout"),

    # Student dashboard + pages
    path("student/dashboard/", student_views.student_dashboard, name="student_dashboard"),
    path("student/dashboard/<str:page>/", student_views.student_dashboard, name="student_dashboard_page"),
    path("student/attendance/", student_views.student_attendance, name="student_attendance"),

    # Teacher dashboard
    path("teacher/dashboard/", teacher_dashboard, name="teacher_dashboard"),
    path("teacher/dashboard/<str:page>/", teacher_dashboard, name="teacher_dashboard_page"),

    # Teacher features
    path("teacher/courses/", manage_courses, name="manage_courses"),
    path("teacher/class/<int:class_number>/", teacher_views.class_dashboard, name="class_dashboard"),
    path('teacher/student/<int:student_id>/attendance/', teacher_views.mark_attendance_student, name='mark_attendance_student'),
    path("profile/", teacher_views.teacher_profile, name="profile"),
    path("teacher/course/<int:course_id>/sessions/", class_sessions, name="class_sessions"),
    path("teacher/course/<int:course_id>/assignments/", teacher_assignments, name="assignments"),
    path("teacher/schedule/", teacher_schedule, name="teacher_schedule"),
    path("teacher/teacher_profile/", teacher_profile, name="teacher_profile"),


    # Admin features
    path("admin/dashboard/", admin_dashboard, name="admin_dashboard"),
]
