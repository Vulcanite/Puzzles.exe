import random
import string
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import customuser
from django.contrib.auth import authenticate, logout, login
import re
from django.contrib import messages

# Create your views here.
def isValid(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return True if re.fullmatch(regex, email) else False

def passwordGenerator():
    return ''.join(random.choice(string.ascii_letters) for i in range(8))


def changePassword(request):
    if request.method == "POST": 
        email = request.user.email
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        current_user = request.user
        print(current_user.check_password(current_password))
        if current_user.check_password(current_password):
            if new_password != confirm_password:
                messages.error(request, "rewrite the correct password")
                return render(request,"changepassword.html")
            current_user.set_password(new_password)
            current_user.save()
            user = authenticate(email = email, password = new_password)
            login(request, user)

            return render(request,'helpdesk/dashboard.html')
        else:
            messages.error(request, "Incorrect password")
            return render(request,"changepassword.html")
    return render(request,"changepassword.html")

def RegisterUser(request):
    if request.method == "POST":              #or True for testing purpose
        email = request.POST.get('email')
        firstname = request.POST.get('first_name')
        lastname = request.POST.get('last_name')
        password = request.POST.get('password')
        role = request.POST.get('role')
        # email = 'amishtp@gmail.com'
        # firstname = "amish"
        # lastname = "tp"
        # password = passwordGenerator()
        # role = '1'
        
        if not isValid(email):
            messages.error(request, "Invalid email")
            return render(request,'register.html')
        if customuser.objects.filter(email=email).exists():
            messages.error(request, "User with this email already exists")
            return render(request,'register.html')

        newUser = customuser(email=email,firstname=firstname,lastname=lastname,role=role)
        newUser.set_password(password)
        newUser.save()
        return redirect("/auth/login")
    return render(request,'register.html')

def LoginUser(request):
    if request.user.is_authenticated:
        user = request.user
        login(request, user)
        user_type = user.role
        if user_type == '1':
            return redirect("/emp/dashboard/")
        elif user_type == '2':
            return redirect("/helpdesk/dashboard/")

    if request.method == "POST":                #or True for testing purpose
        email = request.POST.get('email')
        password = request.POST.get('password')
        # email = 'xyz@gmail.com'
        # password = 'test'

        user = authenticate(email = email, password = password)
        if user is not None:
            login(request, user)
            user_type = user.role
            if user_type == '1':
                return redirect("/emp/dashboard/")
            elif user_type == '2':
                return redirect("/helpdesk/dashboard/")
        else:
            messages.error(request, "Invalid Login Credentials!")
            return redirect("/auth/login")
    
    return render(request, "login.html")

def LogoutUser(request):
    logout(request)
    messages.error(request, "logged out")
    return redirect("/auth/login/")
