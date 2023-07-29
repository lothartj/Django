from django.shortcuts import render, get_object_or_404, redirect
from photoapp.models import Category, Photo

# Create your views here.
def gallery(request):
    categories = Category.objects.all()
    photos = Photo.objects.all()
    context = {'categories':categories, 'photos':photos}
    return render(request, 'photoapp/gallery.html', context)

def viewPhoto(request, pk):
    photo = get_object_or_404(Photo, id=pk)
    context = {'photo':photo}
    return render(request, 'photoapp/photo.html', context)

# views.py
from django.shortcuts import render, redirect
from .models import Category, Photo

def addPhoto(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        data = request.POST
        image = request.FILES.get('image')

        if data['category'] != 'none':
            category_id = int(data['category'])
            category = Category.objects.get(id=category_id)
        elif data['category_new'] != '':
            category, created = Category.objects.get_or_create(name=data['category_new'])
        else:
            category = None

        photo = Photo.objects.create(
            category=category,
            description=data['description'],
            image=image,
        )
        return redirect('gallery')

    context = {'categories': categories}
    return render(request, 'photoapp/add.html', context)


