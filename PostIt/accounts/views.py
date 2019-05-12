from django.shortcuts import render
from accounts.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    
    success_url = reverse_lazy('postitlogin:login')
    template_name = 'signup.html'
    