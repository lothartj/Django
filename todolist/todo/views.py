from django.shortcuts import render, redirect
from .models import Todo

# Create your views here.
def index(request):
    if request.method == 'POST':
        new_todo = Todo(title = request.POST['title'])
        new_todo.save()
        return redirect
    return render(request, 'index.html')