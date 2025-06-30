from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import SignupForm, InquiryForm, UserProfileForm
from .models import Inquiry, UserProfile


# sign in logic
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages

# sign in logic
def signin(request):
    if request.method == 'POST':
        username_or_email = request.POST.get('username')
        password = request.POST.get('password')
        remember = request.POST.get('remember_me')  # <-- capture checkbox

        user = authenticate(request, username=username_or_email, password=password)
        if user is not None:
            login(request, user)

            # Set session expiry
            if not remember:
                request.session.set_expiry(0)  # session expires on browser close
            else:
                request.session.set_expiry(1209600)  # 2 weeks

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


# reset-password logic
def reset_password(request):
    return render(request, 'authenticate/reset_password.html')



# dashboard logic
@login_required
def dashboard(request):
    return render(request, 'main/dashboard.html', {
        'page_title': 'Dashboard'
    })


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
            return redirect('inquiry')
    else:
        form = InquiryForm(instance=latest_inquiry)

    return render(request, 'main/inquiry.html', {
        'form': form,
        'page_title': 'Inquiry'
    })

# inquiry results logic
@login_required
def inquiry_results(request):
    latest_inquiry = Inquiry.objects.filter(user=request.user).order_by('-submitted_at').first()

    if not latest_inquiry:
        messages.info(request, "You haven't submitted any inquiry yet.")
        return redirect('inquiry')

    answers = {
        "Create": [latest_inquiry.create],
        "Study": [latest_inquiry.study],
        "Work(Vocation)": [latest_inquiry.work],
        "Feel": [latest_inquiry.feel],
        "Move(Body)": [latest_inquiry.move],
        "Be(Rest & Soul)": [latest_inquiry.be],
        "Connect": [latest_inquiry.connect]
    }

    return render(request, 'main/inquiry_results.html', {
        "answers": answers,
        "page_title": "Inquiry Results"
    })


# Profile
@login_required
def profile(request):
    user = request.user
    profile, _ = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.username = form.cleaned_data['username']
            user.save()
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('profile')
    else:
        form = UserProfileForm(
            instance=profile,
            initial={
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'username': user.username,
            }
        )

    return render(request, 'main/profile.html', {'form': form})
