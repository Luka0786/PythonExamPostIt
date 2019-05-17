from django.shortcuts import render

from .models import PostModel

# Create your views here.
def posts(request):
    if request.method == 'GET':
        posts = PostModel.objects.all()
        context = {
            'posts': posts
        }
        return render(request, 'posts.html', context)

def your_posts(request):
    if request.method =='GET':
        your_posts = PostModel.objects.filter(user=request.user)
        context = {
            'your_posts': your_posts
        }
        return render(request, 'your_posts.html', context)