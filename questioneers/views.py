from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import SignupForm, InquiryForm
from .models import Inquiry


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


# dashboard logic
@login_required
def dashboard(request):
    return render(request, 'main/dashboard.html')


# inquiry logic
@login_required
def inquiry(request):
    latest_inquiry = Inquiry.objects.filter(user=request.user).order_by('-submitted_at').first()

    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save(commit=False)
            inquiry.user = request.user
            inquiry.save()
            messages.success(request, "Your inquiry was submitted successfully!")
            return redirect('inquiry')  # redirect to same page
    else:
        # Prefill with latest inquiry if exists
        form = InquiryForm(instance=latest_inquiry)

    return render(request, 'main/inquiry.html', {'form': form})