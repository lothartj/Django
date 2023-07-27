from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from .models import Register
from django.contrib import messages 
from django.contrib.auth.hashers import make_password

# Create your views here.
def user_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        hashed_password = make_password(password)


        if not username or not email or not password or not password2:
            messages.error(request, 'All fields are required')
            return render(request, 'retroapp/register.html')


        user_info = Register(username=username,email=email,password=hashed_password,password2=password2)
        user_info.save()
        return redirect('user_home')
    
    return render(request, 'retroapp/register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            messages.error(request, 'All fields are required')

        user = authenticate(username=username,password=password)
        
        if user is not None:
            login(request, user)
            return redirect('user_home')
        else:
            return render(request, 'login.html')
        
    return render(request, 'retroapp/login.html')

def user_home(request):
    return render(request, 'retroapp/home.html')