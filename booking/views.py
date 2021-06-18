from django.shortcuts import redirect, render
from django.template.context_processors import request
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .models import Que_booking
from user.models import User_in_type
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
    user_ty = User_in_type.objects.get(user=current_user)
    day = info.day_open.all()
    typeque = info.type_que.all()
    typeuser = info.type_user.all()
    context = {
        'info' : info,
        'day' : day,
        'typeque' : typeque,
        'typeuser' : typeuser,     
        'current_user': current_user,   
        'user_ty' : user_ty,
        }
    return render(request, template_name='info.html', context=context)


@user_passes_test(lambda u: u.is_authenticated)
@login_required
def create_booking(request, id):
    info = QueInfo.objects.get(pk=id)
    current_user = request.user
    user_type = User_in_type.objects.get(user=current_user)

    if request.method == 'POST':
        if (request.POST.get('phone').isnumeric() == True) and (len(request.POST.get('phone')) == 10):
            booking = Que_booking.objects.create(
            user_id = current_user,
            que_id = info,
            user_type = user_type,
            phone = request.POST.get('phone'),)

            booking.save()
            msg = 'Successfully'
            context = {
               'info' : info,
               'msg' : msg
                }
            return render(request, template_name='create_booking.html', context=context)

        else:
            error = 'กรุณาใส่เบอร์โทรศัพท์ให้ถูกต้อง'
            context = {
                'info' : info,
                'error' : error
                }
            return render(request, template_name='create_booking.html', context=context)
    else:
        booking = Que_booking.objects.none()
    context = {'info' : info, }
    return render(request, template_name='create_booking.html', context=context)


@user_passes_test(lambda u: u.is_authenticated)
@login_required
def my_booking(request):
    current_user = request.user
    my_list = Que_booking.objects.filter(status=1, user_id=current_user)
    my_putoff = Que_booking.objects.filter(status=2, user_id=current_user)
    context = {'my_list' : my_list,'my_putoff' : my_putoff}
    return render(request, template_name='my_booking.html', context=context)


    
@user_passes_test(lambda u: u.is_authenticated)
@login_required
def my_cancel(request,id):
    que_book = Que_booking.objects.get(pk=id)
    que_book.status = 3
    que_book.save()
    return redirect('my_booking')   

@user_passes_test(lambda u: u.is_authenticated)
@login_required
def my_putoff(request,id):
    que_book = Que_booking.objects.get(pk=id)
    que_book.status = 2
    que_book.save()
    return redirect('my_booking')    