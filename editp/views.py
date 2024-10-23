from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from .forms import UserForm, UserProfileForm, CustomPasswordChangeForm

# Create your views here.
@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        password_form = CustomPasswordChangeForm(user=request.user, data=request.POST)

        if user_form.is_valid() and profile_form.is_valid() and password_form.is_valid():
            user_form.save()
            profile_form.save()
            password_form.save()
            update_session_auth_hash(request, password_form.user)  
            return redirect('profile') 

    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.userprofile)
        password_form = CustomPasswordChangeForm(user=request.user)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'password_form': password_form
    }

    return render(request, 'editp/edit_profile.html', context)
