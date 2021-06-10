from django.shortcuts import render
from django.shortcuts import redirect, render
from django.template.context_processors import request
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

# Create your views here.

def login_page(request):
    return render(request, template_name='login.html')

def check_login(request):
    context = {} 
    user = request.user         
    if user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user=user)
            return redirect('index')
        else:
            context['username'] = username
            context['password'] = password
            context['error'] = 'Wrong username or password!'
    return render(request, template_name='login.html', context=context)


def index_page(request):
    return render(request, template_name='index.html')


def logout_page(request):
    auth_logout(request)
    return redirect(to='index')