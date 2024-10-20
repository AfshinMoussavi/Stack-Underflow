from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from users.forms import UserRegisterForm, UserLoginForm, UserUpdateForm
from users.models import User


# Create your views here.
def user_register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Registration successful! Welcome aboard! 🎉')
            
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            login_user = authenticate(request, username=username, password=password)

            if login_user is not None:
                login(request, login_user)
                messages.info(request, f'You are now logged in as {username}.')
                return redirect('users:home')
        else:
            messages.error(request, 'Registration failed. Please check your information and try again.')
    else:
        form = UserRegisterForm()
    
    context = {'form': form}
    return render(request, "user/user_register_form.html", context=context)


def user_login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}! You have successfully logged in.')
                return redirect('users:home')
            else:
                messages.error(request, 'Invalid username or password. Please try again.')
    else:
        form = UserLoginForm()
    
    context = {'form': form}
    return render(request, 'user/user_login_form.html', context)
    

def user_logout_view(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('users:login')


def user_profile_view(request, uid):
    user = get_object_or_404(User, id=uid)
    context = {
        'user':user,
        'uid':uid
    }
    return render(request , "user/user_profile_view.html" , context)


def user_profile_edit_view(request, uid):
    user = get_object_or_404(User, id=uid)
    
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            updated_user = form.save()
            
            if (
                user.username != updated_user.username or 
                user.email != updated_user.email or 
                user.phone_number != updated_user.phone_number or 
                user.national_id != updated_user.national_id
            ):
                messages.success(request, 'Your profile has been successfully updated.')
            else:
                messages.info(request, 'No changes were made to your profile.')
            
            return redirect('users:profile', uid=user.id)
    else:
        form = UserUpdateForm(instance=user)

    context = {
        'form': form,
    }
    return render(request, 'user/user_edit.html', context)


def user_home_view(request):
    return render(request, 'home.html')
