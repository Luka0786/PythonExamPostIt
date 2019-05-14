from django.shortcuts import render, redirect
from accounts.forms import UserCreationForm, EditProfileForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm

def profile(request):
    context = {
        'user': request.user
    }
    return render(request, 'profile.html' ,context)

def edit_profile(request):
    if request.method == "POST":
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('/accounts/profile')

    else:
        form = EditProfileForm(instance=request.user)
        context = {
            'form': form
        }
        return render(request, 'manageprofile.html', context)

class SignUp(generic.CreateView):
    form_class = UserCreationForm
    
    success_url = reverse_lazy('postitlogin:login')
    template_name = 'signup.html'

    
    