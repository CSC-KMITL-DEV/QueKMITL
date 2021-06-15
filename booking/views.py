from django.shortcuts import redirect, render
from django.template.context_processors import request
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from provider.models import Department, QueInfo, TypeUser, Week_Day, TypeQue, Type_in_Dep
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
# Create your views here.

@login_required
@user_passes_test(lambda u: u.is_authenticated)
def all_que(request):
    dep_all = Department.objects.all()
    context = {
        'dep_all' : dep_all
    }
    return render(request, template_name='all_que.html', context=context)

@user_passes_test(lambda u: u.is_authenticated)
@login_required
def type_que(request, id):
    dep = Department.objects.get(pk=id)
    t_in_dep = Type_in_Dep.objects.filter(dep_id=dep.id)
    context = {
        't_in_dep' : t_in_dep,
        'dep' : dep,
    }
    return render(request, template_name='type_que.html', context=context)


@user_passes_test(lambda u: u.is_authenticated)
@login_required
def info_type(request, id):
    tdep = Type_in_Dep.objects.get(pk=id)

    context = {}
    que_list = QueInfo.objects.filter(status=1, type_in_dep_id=tdep)
    que_list = que_list.order_by('date_start')
    context = {
        'que_list' : que_list,
        'tdep' : tdep,
        }
    return render(request, template_name='info_type.html', context=context)




@user_passes_test(lambda u: u.is_authenticated)
@login_required
def info(request, id):
    context = {}
    current_user = request.user
    info = QueInfo.objects.get(pk=id)

    day = info.day_open.all()
    typeque = info.type_que.all()
    typeuser = info.type_user.all()
    context = {
        'info' : info,
        'day' : day,
        'typeque' : typeque,
        'typeuser' : typeuser,     
        'current_user': current_user,   
        }
    return render(request, template_name='info.html', context=context)


@user_passes_test(lambda u: u.is_authenticated)
@login_required
def booking(request, id):
    redirect('my_booking')


@user_passes_test(lambda u: u.is_authenticated)
@login_required
def my_booking(request, id):
    return render(request, template_name='my_booking.html', context=context)