from . import views
from django.urls import path

urlpatterns = [
   path('', views.user_login, name='user_login'),
   path('register/', views.user_register, name='user_register'),
   path('todo/', views.user_todo, name='user_todo'),
]