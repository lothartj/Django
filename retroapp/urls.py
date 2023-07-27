from . import views
from django.urls import path

urlpatterns = [
    path('', views.user_home, name='user_home'),
    path('login/', views.user_login, name='user_login'),
    path('register/', views.user_register, name='user_register')
]
