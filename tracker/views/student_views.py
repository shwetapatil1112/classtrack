from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.http import HttpResponse
import calendar

from tracker.models import Student, Attendance, Course, Enrollment
from tracker.forms import StudentRegistrationForm


# -----------------------
# Home Page
# -----------------------
def home(request):
    return render(request, "tracker/home.html")


# -----------------------
# Student Registration
# -----------------------
class StudentRegisterView(CreateView):
    model = Student
    form_class = StudentRegistrationForm
    template_name = "tracker/register.html"
    success_url = reverse_lazy("student_login")


# -----------------------
# Student Login
# -----------------------
def student_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("student_dashboard")
        messages.error(request, "Invalid credentials")
    return render(request, "tracker/student_login.html")


# -----------------------
# Student Dashboard
# -----------------------
@login_required(login_url="student_login")
def student_dashboard(request, page=None):
    student = Student.objects.filter(user=request.user).first()
    notice = "Next lecture will be online on 30th Aug 2025. Please check your assignments."

    template_map = {
        "attendance": "tracker/content/attendance.html",
        "classroom": "tracker/content/classroom.html",
        "profile": "tracker/content/profile.html",
        "assignments": "tracker/content/assignments.html",
        "tests": "tracker/content/tests.html",
        "learning": "tracker/content/learning.html",
        "calendar": "tracker/content/calendar.html",
    }

    if page:
        template_name = template_map.get(page)
        if not template_name:
            return HttpResponse("Page not found", status=404)

        context = {"student": student}

        if page == "calendar":
            year = 2025
            cal = calendar.Calendar(firstweekday=6)  # Sunday first
            calendar_data_list = []
            for month in range(1, 13):
                calendar_data_list.append({
                    "number": month,
                    "name": calendar.month_name[month],
                    "weeks": cal.monthdayscalendar(year, month)
                })
            context["calendar_data_list"] = calendar_data_list

        return render(request, template_name, context)

    return render(request, "tracker/student_dashboard.html", {
        "student": student,
        "notice": notice
    })


# -----------------------
# Student Attendance
# -----------------------
@login_required(login_url='student_login')
def student_attendance(request):
    student = get_object_or_404(Student, user=request.user)
    attendance_records = Attendance.objects.filter(student=student).order_by('-session__date')

    total_classes = attendance_records.count()
    present_classes = attendance_records.filter(status='P').count()
    attendance_percentage = int((present_classes / total_classes) * 100) if total_classes else 0

    return render(request, 'tracker/content/student_attendance.html', {
        'student': student,
        'attendance_records': attendance_records,
        'attendance_percentage': attendance_percentage
    })


# -----------------------
# Student Detail
# -----------------------
@login_required(login_url="student_login")
def detail(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    return render(request, "tracker/student_detail.html", {"student": student})
