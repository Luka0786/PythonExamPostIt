from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator

# Create your models here.
class CommentModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField(validators=[MaxLengthValidator(1000)]) #1/3 of a page


class PostModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    body = models.TextField(validators=[MaxLengthValidator(3000)]) #3000 characters = one page 

    comments = models.ManyToManyField(CommentModel) 
    def __str__(self):
        return self.title

class DraftModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    body = models.TextField(validators=[MaxLengthValidator(3000)]) #3000 characters = one page 
