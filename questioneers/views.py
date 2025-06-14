from django.shortcuts import render

# Create your views here.
def signin(request):
    return render(request, 'authenticate/signin.html')
    

def signup(request):
    return render(request, 'authenticate/signup.html')


def dashboard(request):
    return render(request, 'main/dashboard.html')


def inquiry(request):
    return render(request, 'main/inquiry.html')