from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import SignupForm


# sign in logic
def signin(request):
    if request.method == 'POST':
        username_or_email = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username_or_email, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials')

    return render(request, 'authenticate/signin.html')
    

# sign up logic
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = SignupForm()
    return render(request, 'authenticate/signup.html', {'form': form})


# sign out logic
def signout(request):
    logout(request)
    return redirect('signin')


@login_required
def dashboard(request):
    return render(request, 'main/dashboard.html')


@login_required
def inquiry(request):
    return render(request, 'main/inquiry.html')