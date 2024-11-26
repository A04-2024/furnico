from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from .forms import UserForm, UserProfileForm, CustomPasswordChangeForm

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from .models import UserProfile
from django.contrib.auth.decorators import user_passes_test

# Create your views here.
def is_admin(user):
    return user.is_superuser or (hasattr(user, 'userprofile') and user.userprofile.role == 'admin')

@user_passes_test(is_admin)
def admin_only_view(request):
    return render(request, 'admin_page.html')

@login_required
def edit_profile(request):
    user = request.user
    if not hasattr(user, 'userprofile'):
        UserProfile.objects.create(user=user)
    
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)

        profile_form = UserProfileForm(request.POST, request.FILES, instance=user.userprofile)
        if not is_admin(user):
            profile_form.fields.pop('role') 
        
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
        if not is_admin(user):
            profile_form.fields.pop('role') 
        password_form = CustomPasswordChangeForm(user=user)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'password_form': password_form
    }

    return render(request, 'editprofile.html', context)

def register(request):
    if request.method == "POST":
        user_form = UserCreationForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = user.userprofile
            profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
            profile_form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('editp:login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        user_form = UserCreationForm()
        profile_form = UserProfileForm()
    context = {'user_form': user_form, 'profile_form': profile_form}
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