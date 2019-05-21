from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from accounts.forms import UserCreationForm, EditProfileForm, EditAvatar
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm

@login_required
def profile(request):
    context = {
        'user': request.user
    }
    return render(request, 'profile.html', context)
    
@login_required
def edit_profile(request):
    if request.method == "POST":
        form = EditProfileForm(request.POST, instance=request.user)
        profile_form = EditAvatar(request.POST, request.FILES, instance=request.user.userprofile)

        if form.is_valid() and profile_form.is_valid():
            user_form = form.save()
            custom_form = profile_form.save()
            return redirect('/accounts/profile')

    else:
        print('else')
        form = EditProfileForm(instance=request.user)
        profile_form = EditAvatar(instance=request.user.userprofile)
        args = {'form': form, 
        'profile_form': profile_form
        }
        # args.update(csrf(request))
        #args['form'] = form
        #args['profile_form'] = profile_form
        return render(request, 'manageprofile.html', args)
        


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    
    success_url = reverse_lazy('postitlogin:login')
    template_name = 'signup.html'

    
    