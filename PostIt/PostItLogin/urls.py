from django.urls import path, include

# . means the package im in right now
from . import views

app_name = 'PostItLogin'

urlpatterns = [
    path('', include('PostItApp.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]