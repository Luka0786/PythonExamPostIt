from django.urls import path, include
from django.views.generic.base import TemplateView

# . means the package im in right now
from . import views

app_name = 'postitapp'

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
]