from django.shortcuts import render, redirect
from .models import Todo
# Create your views here.
def user_todo(request):
    if request.method == 'POST':
        task = request.POST.get('task')

        save = Todo(task=task)
        save.save()
        
    user_tasks = Todo.objects.all()
    return render(request, 'todoapp/todo.html', {'user_tasks': user_tasks})

def delete_task(request, task_id):
    print("Task ID to delete:", task_id)
    task = Todo.objects.get(pk=task_id)
    task.delete()
    return redirect('todo')

def finish_task(request, task_id):
    task = Todo.objects.get(pk=task_id)
    task.status = "Finished"
    task.save()
    return redirect('todo')
