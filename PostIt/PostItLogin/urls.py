from django.urls import path, include

# . means the package im in right now
from . import views

app_name = 'postitlogin'

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
]