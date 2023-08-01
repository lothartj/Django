from . import views
from django.urls import path

urlpatterns = [
    path('', views.user_todo, name='todo'),
    path('delete_task/<int:task_id>/', views.delete_task, name='delete_task'),
    path('finish_task/<int:task_id>/', views.finish_task, name='finish_task'),

]
