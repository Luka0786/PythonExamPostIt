from django.urls import path, include
from django.views.generic.base import TemplateView

# . means the package im in right now
from . import views

app_name = 'postitapp'

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('posts', views.posts, name='posts'),
    path('posts/create', views.create_post, name="create_post"),
    path('posts/yours', views.your_posts, name="your_posts"),
    path('posts/<int:pk>', views.post, name="post"),
    path('post/comment', views.create_comment, name="create_comment"),
    path('posts/drafts', views.your_drafts, name="your_drafts"),
    path('posts/draft/<int:pk>', views.draft, name="draft")
]