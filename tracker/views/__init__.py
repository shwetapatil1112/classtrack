# tracker/views/__init__.py

# -----------------------
# Student Views
# -----------------------
from .student_views import (
    home,
    student_login,
    student_dashboard,
    student_attendance,
    detail,
    StudentRegisterView,
)

# -----------------------
# Teacher Views
# -----------------------
from .teacher_views import (
    teacher_register,
    teacher_login,
    teacher_dashboard,
    mark_attendance,
    attendance_summary,
    manage_courses,
    class_sessions,
    teacher_assignments,
    teacher_schedule,
    teacher_profile,
)

# -----------------------
# Admin Views
# -----------------------
from .admin_views import (
    admin_login,
    admin_dashboard,
)
