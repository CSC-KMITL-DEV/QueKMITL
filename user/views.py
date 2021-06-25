from django.shortcuts import render
from django.shortcuts import redirect, render
from django.template.context_processors import request
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from .models import User_in_type, User_punish
from django.contrib.auth import authenticate, login
from provider.models import TypeUser
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
# Create your views here.

def login_page(request):
    return render(request, template_name='login.html')

def check_login(request):
    context = {} 
    user = request.user         
    if user.is_authenticated:
        return redirect('index')
    
    if user.is_superuser or user.is_staff:
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
    check_user_in = User_in_type.objects.all()
    punish = User_punish.objects.all()
    try:
        
        if request.user.is_authenticated:
            user_id = request.user
            user_id = user_id.id
            user = User.objects.get(pk=user_id)
            count = 0
            for p in punish:
                if p.user == user:
                    count += 1
            
            if count == 0:
                create = User_punish.objects.create(
                        user = user,
                    )
                create.save()
            else:
                create = User_punish.objects.none()

                
            if user not in check_user_in:
                email = user.email
                username = email.split('@')[0]
                domain = email.split('@')[1]
                domain_name = domain.split('.')[0]
                kmitl = 'kmitl'
                if username.isnumeric() and (domain_name == kmitl):
                    create = User_in_type(
                        user = user,
                        user_type = TypeUser.objects.get(id=2)
                    )
                    create.save()
                elif username.isalpha() and (domain_name == kmitl):
                    create = User_in_type.objects.create(
                        user = user,
                        user_type = TypeUser.objects.get(id=1)
                        )
                    create.save()
                    
                else:
                    create = User_in_type.objects.create(
                        user = user,
                        user_type = TypeUser.objects.get(id=3)
                        )
                    create.save()
                return render(request, template_name='index.html')


    except IntegrityError as e:
        user_info = User_in_type.objects.get(user=user)

    return render(request, template_name='index.html')


def logout_page(request):
    auth_logout(request)
    return redirect(to='index')


@login_required
@user_passes_test(lambda u: u.is_authenticated)
def profile(request, id):
    user = User.objects.get(pk=id)
    user_info = User_in_type.objects.get(user=user)
    user_punish = User_punish.objects.get(user=user)
    context = {
        'user_info': user_info,
        'user' : user,
        'user_punish' : user_punish
    }  
       

    return render(request, template_name='profile.html', context=context)


