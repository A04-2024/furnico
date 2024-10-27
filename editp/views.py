from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from .forms import UserForm, UserProfileForm, CustomPasswordChangeForm

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from .models import UserProfile

# Create your views here.
@login_required
def edit_profile(request):
    user = request.user
    # Ensure the user has a UserProfile instance
    if not hasattr(user, 'userprofile'):
        UserProfile.objects.create(user=user)
    
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user.userprofile)
        password_form = CustomPasswordChangeForm(user=user, data=request.POST)

        if user_form.is_valid() and profile_form.is_valid() and password_form.is_valid():
            user_form.save()
            profile_form.save()
            password_form.save()
            update_session_auth_hash(request, password_form.user)  
            messages.success(request, 'Profil Anda telah berhasil diperbarui!')
            return redirect('show_products:show_main') 

    else:
        user_form = UserForm(instance=user)
        profile_form = UserProfileForm(instance=user.userprofile)
        password_form = CustomPasswordChangeForm(user=user)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'password_form': password_form
    }

    return render(request, 'editprofile.html', context)

def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('editp:login')
    context = {'form':form}
    return render(request, 'register.html', context)

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('show_products:show_main')

    else:
      form = AuthenticationForm(request)
    context = {'form': form}
    return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    return redirect('editp:login')