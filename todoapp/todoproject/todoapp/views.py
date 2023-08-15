from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from django.contrib import messages
from .models import Register, Todo

# Create your views here.
def user_register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if not name or not surname or not email or not password or not password2:
            messages.error(request, 'Please fill in all fields')
            return redirect('register')  # Assuming you want to redirect back to the registration page
        elif password != password2:
            messages.error(request, 'Passwords do not match')
            return redirect('register')
        else:
            user = Register(email=email, password=password, name=name, surname=surname)
            user.save()
            return redirect('user_todo')


    return render(request, 'todoapp/register.html')


def user_login(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')

        user = authenticate(name=name,password=password)
        if user is not None:
            login(request, user)

        return redirect('user_todo')

    return render(request, 'todoapp/login.html')

@login_required(login_url='user_login')
def user_todo(request, item_id):
    if request.method == 'POST':
        task = request.POST.get('task')

        todo = Todo(task=task)
        todo.save()
        todo.delete()

    todos = Todo.objects.all(id=item_id)
    return render(request, 'todoapp/todo.html', {'todos':todos})