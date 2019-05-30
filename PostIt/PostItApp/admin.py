from django.contrib import admin
from .models import PostModel, CommentModel, DraftModel

# Register your models here.
admin.site.register(PostModel)
admin.site.register(CommentModel)
admin.site.register(DraftModel)
