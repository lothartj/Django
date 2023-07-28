from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.user_home, name='user_home'),
    path('login/', views.user_login, name='user_login'),
    path('register/', views.user_register, name='user_register'),
    path('image/', views.user_image, name='user_image')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)