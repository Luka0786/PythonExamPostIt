from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class PostModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    body = models.TextField(max_length=3000) #3000 characters = one page 

    def __str__(self):
        return self.title

class CommentModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    post = models.OneToOneField(PostModel, on_delete=models.CASCADE)
    body = models.TextField(max_length=1000) #1/3 of a page

    def __str__(self):
        return self.post.title + ' : ' + self.user.username


