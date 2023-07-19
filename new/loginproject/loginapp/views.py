from django.shortcuts import render
from .models import Login
# Create your views here.
def login(request):
    if request.method =='POST':
        username= request.POST['username']
        password= request.POST['password']
        save = Login(username=username,password=password)
        save.save()
    info = Login.objects.all()
    context = {'info':info}
    return render(request, 'loginapp/login.html',context) 