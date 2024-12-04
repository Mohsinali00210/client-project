from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from .forms import RegisterForm, LoginForm
from django.http import JsonResponse
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from rest_framework import status
# Register View
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Account created successfully')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

# Login View
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                response = HttpResponse("Cookie has been set")
                response.set_cookie('user_id1', user.id, max_age=3600)
                
                return redirect('my_collections')  # Redirect to home or any other page
            else:
                messages.error(request, 'Invalid username or password')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


# Logout View (Optional)
def logout_view(request):
    auth_logout(request)
    return redirect('login')


def test_view(request):
    return render(request, 'tokenTest.html')

def isUserLoggedIn(request):
    # Safely get the user_id from cookies
    user_id = request.COOKIES.get('user_id', '')

    # If user_id is an empty string, treat it as "not logged in"
    if user_id != "":
        return JsonResponse({'user_id': user_id}, status=status.HTTP_200_OK)
    else:
        return JsonResponse({'user_id': ""}, status=status.HTTP_401_UNAUTHORIZED)
    