from django.urls import path, reverse_lazy, include
from django.contrib.auth import views as auth_views
# . means the package im in right now
from . import views

app_name = 'postitlogin'

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
]