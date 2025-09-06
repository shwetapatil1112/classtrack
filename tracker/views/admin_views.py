from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# -----------------------
# Admin Login
# -----------------------
def admin_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user and user.is_staff:  # only staff/admins
            login(request, user)
            return redirect("admin_dashboard")
        messages.error(request, "Invalid admin credentials")
    return render(request, "tracker/admin_login.html")


# -----------------------
# Admin Dashboard
# -----------------------
@login_required(login_url="admin_login")
def admin_dashboard(request):
    return render(request, "tracker/admin_dashboard.html")
