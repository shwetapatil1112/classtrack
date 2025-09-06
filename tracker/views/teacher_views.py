from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from tracker.models import TeacherProfile, Course, Student, Attendance, ClassSession
from tracker.forms import TeacherRegistrationForm

# -----------------------
# Teacher Registration
# -----------------------
def teacher_register(request):
    if request.method == "POST":
        form = TeacherRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Teacher registered successfully! Please log in.")
            return redirect("teacher_login")
    else:
        form = TeacherRegistrationForm()

    return render(request, "tracker/register.html", {
        "form": form,
        "title": "Teacher Registration"
    })

# -----------------------
# Teacher Login
# -----------------------
def teacher_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if hasattr(user, "teacherprofile"):
                login(request, user)
                return redirect("teacher_dashboard")
            else:
                messages.error(request, "Not a teacher account.")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "tracker/teacher_login.html")


# -----------------------
# Teacher Dashboard
# -----------------------
@login_required(login_url="teacher_login")
def teacher_dashboard(request):
    courses = Course.objects.filter(teacher=request.user)
    return render(request, "tracker/teacher_dashboard.html", {"courses": courses})


# -----------------------
# Class Dashboard (Students list)
# -----------------------
@login_required(login_url="teacher_login")
def class_dashboard(request, class_number):
    # Filter courses by class_number
    courses = Course.objects.filter(teacher=request.user, class_number=class_number)
    
    # Get all students enrolled in those courses
    students = Student.objects.filter(enrollments__course__in=courses).distinct()
    
    return render(request, "tracker/content/class_dashboard.html", {
        "class_number": class_number,
        "students": students
    })


# -----------------------
# Mark Attendance for an entire course
# -----------------------
@login_required(login_url='teacher_login')
def mark_attendance(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    students = [enrollment.student for enrollment in course.enrollments.all()]

    if request.method == "POST":
        date = request.POST.get('date', timezone.localdate())
        session, created = ClassSession.objects.get_or_create(
            course=course, date=date, defaults={'created_by': request.user}
        )

        for student in students:
            status = request.POST.get(f'status_{student.id}', 'A')  # Default Absent
            Attendance.objects.update_or_create(
                session=session,
                student=student,
                defaults={'status': status, 'marked_by': request.user}
            )
        messages.success(request, f"Attendance marked for {course.name} on {date}")
        return redirect('teacher_dashboard')

    return render(request, 'tracker/contents/mark_attendance.html', {
        'course': course,
        'students': students,
    })


# -----------------------
# Mark Attendance for a single student
# -----------------------
@login_required(login_url='teacher_login')
def mark_attendance_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    courses = Course.objects.filter(teacher=request.user, enrollments__student=student).distinct()

    if request.method == "POST":
        course_id = request.POST.get('course_id')
        course = get_object_or_404(Course, id=course_id)
        date = request.POST.get('date', timezone.localdate())
        session, created = ClassSession.objects.get_or_create(
            course=course, date=date, defaults={'created_by': request.user}
        )
        status = request.POST.get('status', 'A')  # Default Absent
        Attendance.objects.update_or_create(
            session=session,
            student=student,
            defaults={'status': status, 'marked_by': request.user}
        )
        messages.success(request, f"Attendance updated for {student.full_name}")
        return redirect('class_dashboard', class_number=course.name.split('th')[0])

    return render(request, 'tracker/contents/mark_attendance_student.html', {
        'student': student,
        'courses': courses
    })


# -----------------------
# Attendance Summary for a course
# -----------------------
@login_required(login_url='teacher_login')
def attendance_summary(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    students = [enrollment.student for enrollment in course.enrollments.all()]

    summary = []
    for student in students:
        total_sessions = Attendance.objects.filter(student=student, session__course=course).count()
        present_sessions = Attendance.objects.filter(student=student, session__course=course, status='P').count()
        summary.append({
            'student': student,
            'total_sessions': total_sessions,
            'present_sessions': present_sessions,
            'attendance_percentage': (present_sessions / total_sessions * 100) if total_sessions else 0
        })

    return render(request, 'tracker/contents/attendance_summary.html', {
        'course': course,
        'summary': summary
    })


# -----------------------
# Manage Courses
# -----------------------
@login_required(login_url="teacher_login")
def manage_courses(request):
    courses = Course.objects.filter(teacher=request.user)
    return render(request, "tracker/contents/manage_courses.html", {"courses": courses})


# -----------------------
# Class Sessions
# -----------------------
@login_required(login_url="teacher_login")
def class_sessions(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    sessions = ClassSession.objects.filter(course=course).order_by('-date')
    return render(request, "tracker/contents/class_sessions.html", {
        "course": course,
        "sessions": sessions
    })


# -----------------------
# Teacher Assignments
# -----------------------
@login_required(login_url="teacher_login")
def teacher_assignments(request, course_id):
    course = get_object_or_404(Course, id=course_id, teacher=request.user)
    return render(request, "tracker/contents/teacher_assignments.html", {"course": course})


# -----------------------
# Teacher Schedule
# -----------------------
@login_required(login_url="teacher_login")
def teacher_schedule(request):
    courses = Course.objects.filter(teacher=request.user)
    return render(request, "tracker/contents/schedule.html", {"courses": courses})


# -----------------------
# Teacher Profile
# -----------------------


@login_required(login_url="teacher_login")
def teacher_profile(request):
    teacher = TeacherProfile.objects.filter(user=request.user).first()
    return render(request, "tracker/contents/teacher_profile.html", {"teacher": teacher})
