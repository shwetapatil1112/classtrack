from django import forms
from django.contrib.auth import get_user_model
from django.db import transaction
from .models import Student, TeacherProfile,Course
import uuid
from django.contrib.auth.forms import UserCreationForm


User = get_user_model()

# -----------------------
# Student Registration (your existing code)
# -----------------------
class StudentRegistrationForm(forms.ModelForm):
    # --- User fields ---
    first_name = forms.CharField(max_length=30, required=True, label="First Name")
    last_name = forms.CharField(max_length=30, required=True, label="Last Name")
    username = forms.CharField(max_length=150, required=False, help_text="Leave blank to auto-generate")
    email = forms.EmailField(required=False, help_text="Optional")

    # --- Student-specific fields ---
    roll_no = forms.CharField(max_length=50, required=True, label="Roll Number")
    gender = forms.ChoiceField(
        choices=(("Male", "Male"), ("Female", "Female"), ("Other", "Other")),
        required=False,
    )
    parent_phone = forms.CharField(max_length=15, required=False)
    address = forms.CharField(widget=forms.Textarea, required=False)
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}), required=False)
    course = forms.ModelChoiceField(queryset=Course.objects.all(), empty_label="Select Course")
    profile_photo = forms.ImageField(required=False)

    # --- Password fields ---
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = Student
        fields = [
            "first_name", "last_name", "username", "email",
            "roll_no", "gender", "parent_phone", "address",
            "date_of_birth", "course", "profile_photo",
            "password1", "password2",
        ]

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("password1") != cleaned.get("password2"):
            raise forms.ValidationError("Passwords do not match")
        username = cleaned.get("username")
        if username and User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        email = cleaned.get("email")
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return cleaned

    def save(self, commit=True):
        with transaction.atomic():
            username = self.cleaned_data.get("username") or str(uuid.uuid4())[:8]
            email = self.cleaned_data.get("email") or None
            user = User.objects.create_user(
                username=username,
                email=email,
                first_name=self.cleaned_data["first_name"],
                last_name=self.cleaned_data["last_name"],
                password=self.cleaned_data["password1"],
            )
            student = super().save(commit=False)
            student.user = user
            if commit:
                student.save()
            return student

class TeacherRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    employee_id = forms.CharField(max_length=50, required=True)
    department = forms.CharField(max_length=100, required=False)
    phone = forms.CharField(max_length=15, required=False)
    address = forms.CharField(widget=forms.Textarea, required=False)
    profile_photo = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            TeacherProfile.objects.create(
                user=user,
                employee_id=self.cleaned_data["employee_id"],
                department=self.cleaned_data.get("department"),
                phone=self.cleaned_data.get("phone"),
                address=self.cleaned_data.get("address"),
                profile_photo=self.cleaned_data.get("profile_photo"),
            )
        return user
