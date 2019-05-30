from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.urls import reverse, resolve
from django.core.mail import send_mail


from .models import PostModel, CommentModel, DraftModel


# Create your views here.
@login_required
def posts(request):
    if request.method == 'GET':
        posts = PostModel.objects.all()
        context = {
            'posts': posts
        }
        return render(request, 'posts.html', context)

@login_required
def your_posts(request):
    if request.method =='GET':
        your_posts = PostModel.objects.filter(user=request.user)
        context = {
            'your_posts': your_posts
        }
        return render(request, 'your_posts.html', context)

@login_required
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

@login_required
def create_post(request):
    if request.method == 'GET':
        return render(request, 'create_post.html')
    
    if request.method == 'POST':
        post = PostModel()
        post.user = request.user
        post.title = request.POST['title']
        post.body = request.POST['body']
        
        print(len(post.title))
        print(len(post.body))
        if(len(post.title) > 30 or len(post.body) > 3000):
                    
            context = {
                'error': 'Post too long. Title max length is 30 characters! Body max length is 3000 characters!',
                
            }
            return render(request, 'create_post.html', context)
        else:
            post.save()
            return HttpResponseRedirect(reverse('postitapp:home'))
    
    return HttpResponseBadRequest()

@login_required
def notify_poster(post, comment):
    send_mail(
            'Someone commented on your post',
            'Your post ' + post.title + ' got a new comment! ' + 'User ' + comment.user.username + ' commented on your post! ',
            'postitpython@gmail.com',
            [post.user.email],
            fail_silently=False,
        )
    

def your_drafts(request):
    if request.method == 'GET':
        your_drafts = DraftModel.objects.filter(user=request.user)
        context = {
            'your_drafts': your_drafts
        }
        return render(request, 'your_drafts.html', context)

def draft(request, pk):
    draft = get_object_or_404(DraftModel, pk=pk)
        
    if request.method == 'GET':
        context = {
            'draft': draft,
        }

        return render(request, 'post.html', context)

@login_required
def create_comment(request):
    if request.method == 'GET':
        return render(request, 'posts.html')
    
    if request.method == 'POST':
        post_id = request.POST['id']
        post = get_object_or_404(PostModel, pk=post_id)
        comment = CommentModel()
        comment.user = request.user
        comment.body = request.POST['text']
  
        if(len(comment.body) > 1000):
            
            context = {
                'error': 'Comment too long. Max length is 1000 characters!',
                'post': post,
                'comments': post.comments.all()
            }
        else:
            comment.save()
            post.comments.add(comment)
            notify_poster(post, comment)
            context = {
                'post': post,
                'comments': post.comments.all()
            }   
        

        return render(request, 'post.html', context)
    
    return HttpResponseBadRequest()