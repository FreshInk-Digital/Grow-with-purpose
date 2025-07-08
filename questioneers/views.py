from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .forms import SignupForm, InquiryForm, UserProfileForm
from .models import Inquiry, UserProfile


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
    if request.method == 'POST':
        email = request.POST.get('email')
        users = User.objects.filter(email=email)

        if users.exists():
            user = users.first()
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            reset_link = request.build_absolute_uri(
                f"/reset/{uid}/{token}/"
            )

            subject = "Reset Your Password"
            message = render_to_string("authenticate/password_reset_email.html", {
                "user": user,
                "reset_link": reset_link,
            })

            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
            messages.success(request, "A reset password link has been sent.")
            return redirect('reset-password')
        else:
            messages.success(request, "If your email is registered, a reset link has been sent.")
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


@login_required
def inquiry_all_results(request):
    inquiries = Inquiry.objects.filter(user=request.user).order_by('-submitted_at')
    return render(request, 'main/inquiry_all_results.html', {
        'inquiries': inquiries,
        'page_title': 'All Past Inquiries'
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
