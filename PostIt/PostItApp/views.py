from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.urls import reverse, resolve
from .models import PostModel, CommentModel


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

def post(request, pk):
    post = get_object_or_404(PostModel, pk=pk)
    comments_list = []
    for p in CommentModel.objects.raw('SELECT * FROM postitapp_postmodel_comments WHERE postmodel_id = %s' % post.id):
        comments_list.append(p)
        
    #comments = CommentModel.objects.all().filter(id=1)
    if request.method == 'GET':
        context = {
            'post': post,
            'comments': comments_list
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



def create_comment(request):
    if request.method == 'GET':
        return render(request, 'posts.html')
    
    if request.method == 'POST':
        post_id = request.POST['id']
        post = get_object_or_404(PostModel, pk=post_id)
        comment = CommentModel()
        comment.user = request.user
        comment.body = request.POST['text']
        comment.save()
        post.comments.add(comment)
        
        
        
        context = {
            'post': post,
            'comments': post.comments.all()
        }

        return render(request, 'post.html', context)
    
    return HttpResponseBadRequest()