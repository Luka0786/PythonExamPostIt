from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.urls import reverse

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

def post(request):
    if request.method == 'GET':
        context = {
            'post': request.post
        }
        return render(request, 'post.html', context)

def create_post(request):
    if request.method == 'GET':
        return render(request, 'create_post.html')
    
    if request.method == 'POST':
        post = PostModel()
        post.user = request.user
        post.title = request.POST['title']
        post.body = request.POST['body']
        post.save()
        return HttpResponseRedirect(reverse('postitapp:home'))
    
    return HttpResponseBadRequest()

"""def create_comment(request):
    if request.method == 'GET':
        return render(request, 'todoapp/new.html')
    
    if request.method == 'POST':
        todo = Todo()
        todo.user = request.user
        todo.text = request.POST['text']
        completed = request.POST.getlist('completed')
        if len(completed) > 0:
            todo.completed = True
        else:
            todo.completed = False
        todo.save()
        return HttpResponseRedirect(reverse('todoapp:index'))
    
    return HttpResponseBadRequest()"""