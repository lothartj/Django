from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import Register,Login
# Create your views here.
def userlogin(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        username = request.POST.get('username') 
        password = request.POST.get('password') 

        user = authenticate(request, id=id,username=username,password=password)

        if user is not None:
            login(request, user)
            print(id)

            return redirect('home')
        
    return render(request, 'registera/login.html')

from django.contrib import messages

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if any of the fields are empty
        if not username or not email or not password:
            messages.error(request, 'All fields are required.')
            return render(request, 'registera/register.html')

        user_register = Register(username=username, email=email, password=password)
        user_register.save()
        return redirect('home')

    return render(request, 'registera/register.html')


def home(request):
    return render(request, 'registera/home.html')