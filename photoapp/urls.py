from . import views
from django.urls import path

urlpatterns = [
    path('', views.gallery, name="gallery"),
    path('photo/<str:pk>/', views.viewPhoto, name="photo"),
    path('add/', views.addPhoto, name="add"),
]
