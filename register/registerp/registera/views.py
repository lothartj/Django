from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import Register

# Create your views here.
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        save = Register(username=username,email=email,password=password,password2=password2)
        save.save()
        return redirect('home')

    return render(request, 'registera/register.html')

def home(request):
    registrations = Register.objects.all()
    return render(request, 'registera/home.html', {'registrations':registrations})

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # If the user is found in the database and the credentials are valid, log the user in
            login(request, user)
            # Redirect to the home page or any other page after successful login
            return redirect('home')
        else:
            # If the user is not found in the database or the credentials are invalid,
            # handle the authentication failure (e.g., display an error message)
            # For simplicity, you can just render the login page again with an error message
            error_message = "Invalid username or password. Please try again."
            return render(request, 'registera/login.html', {'error_message': error_message})
        
    return render(request, 'registera/login.html')