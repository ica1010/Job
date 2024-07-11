from pyexpat.errors import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate , login , logout
from django.contrib import messages
from django.contrib.auth.models import User
from user.models import ProfileEmployeur

# Create your views here.

def register_view(request):
    url = request.META.get('HTTP_REFERER')

    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in.')
        return redirect('home')
    
    elif request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already in use.')
        else:
            try:
                user = User.objects.create_user(username=email, email=email, password=password)
                messages.success(request, 'Account created successfully!')
                user.is_staff = True
                user.is_superuser = True
                user.save()

                ProfileEmployeur.objects.create(user=user)
                login(request, user)
                return redirect('home')
            except Exception as e :
                messages.error(request, f'Erreur :{e}')
                return url


    return render (request, 'auth/signup.html')    



def login_view(request):
    # url = request.META.get('HTTP_REFERER')

    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in.')
        return redirect('homePage')
    
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
           
        user = authenticate(request, username=username, password=password)
        messages.success(request, 'Login successfully!')
        login(request, user)
        return redirect('home')

    return render(request, 'auth/login.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'you are now logged out ')
    return redirect('home')  