from django.conf import settings
from django.db import models
from django.utils import timezone

User = settings.AUTH_USER_MODEL


# -----------------------
# Course
# -----------------------
class Course(models.Model):
    name = models.CharField(max_length=120)
    code = models.CharField(max_length=20, unique=True)
    class_number = models.IntegerField(null=True, blank=True)  # <-- add this
    description = models.TextField(blank=True)
    teacher = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="courses_taught"
    )
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)


    def __str__(self):
        return self.name 




# -----------------------
# Student
# -----------------------
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    enrollment_number = models.CharField(max_length=50, unique=True, null=True, blank=True)
    email = models.EmailField(blank=True, null=True)
    profile_photo = models.ImageField(upload_to="profiles/", blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True, related_name="students")
    gender = models.CharField(
        max_length=10,
        choices=[("Male", "Male"), ("Female", "Female"), ("Other", "Other")],
        blank=True,
        null=True,
    )
    date_of_birth = models.DateField(blank=True, null=True)
    parent_phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["enrollment_number"]

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.enrollment_number})"

    @property
    def full_name(self):
        return self.user.get_full_name()



# -----------------------
# Teacher Model
# -----------------------
class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=50, unique=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    profile_photo = models.ImageField(upload_to="teachers/", blank=True, null=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.employee_id}"



# -----------------------
# Enrollment
# -----------------------
class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="enrollments")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="enrollments")
    joined_on = models.DateField(default=timezone.now)

    class Meta:
        unique_together = ("student", "course")

    def __str__(self):
        return f"{self.student.full_name} -> {self.course.code}"


# -----------------------
# ClassSession
# -----------------------
class ClassSession(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="sessions")
    topic = models.CharField(max_length=200, blank=True)
    date = models.DateField(default=timezone.localdate)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date", "-id"]

    def __str__(self):
        return f"{self.course.code} {self.date}"


# -----------------------
# Attendance
# -----------------------
class Attendance(models.Model):
    PRESENT = "P"
    ABSENT = "A"
    LATE = "L"
    EXCUSED = "E"

    STATUS_CHOICES = [
        (PRESENT, "Present"),
        (ABSENT, "Absent"),
        (LATE, "Late"),
        (EXCUSED, "Excused"),
    ]

    session = models.ForeignKey(ClassSession, on_delete=models.CASCADE, related_name="attendance")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="attendance")
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=PRESENT)
    marked_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    marked_at = models.DateTimeField(auto_now_add=True)
    notes = models.CharField(max_length=200, blank=True)

    class Meta:
        unique_together = ("session", "student")

    def __str__(self):
        return f"{self.student.full_name} - {self.get_status_display()} on {self.session.date}"

class mark_attendance(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=[('Present','Present'),('Absent','Absent')])
    
    class Meta:
        unique_together = ('student', 'course', 'date')

    def __str__(self):
        return f"{self.student} - {self.course} - {self.date}"
