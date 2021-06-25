from django.shortcuts import redirect, render
from django.template.context_processors import request
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .models import Que_booking, Que_walkin
from user.models import User_in_type
from provider.models import Department, QueInfo, TypeUser, Week_Day, TypeQue, Type_in_Dep
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Max

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
    user_ty = user_ty.user_type
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
    w = Que_walkin.objects.all().count()
    qb = Que_booking.objects.all().count()

    if request.method == 'POST':
        if (request.POST.get('phone').isnumeric() == True) and (len(request.POST.get('phone')) == 10):

            if (w == 0) and (qb == 0):
                booking = Que_booking.objects.create(
                user_id = current_user,
                que_id = info,
                user_type = user_type,
                rang = 1,
                phone = request.POST.get('phone'),)

                booking.save()
                msg = 'Successfully'
                context = {
                'info' : info,
                'msg' : msg
                    }
                return render(request, template_name='create_booking.html', context=context)

            if (w != 0) and (qb == 0):
                qw = Que_walkin.objects.all().aggregate(Max('rang')).get('rang__max')
                value = qw
                booking = Que_booking.objects.create(
                user_id = current_user,
                que_id = info,
                user_type = user_type,
                rang = value + 1,
                phone = request.POST.get('phone'),)

                booking.save()
                msg = 'Successfully'
                context = {
                'info' : info,
                'msg' : msg
                    }
                return render(request, template_name='create_booking.html', context=context)

            if (qb != 0) and (w == 0):
                q_b = Que_booking.objects.all().aggregate(Max('rang')).get('rang__max')
                value = q_b
                booking = Que_booking.objects.create(
                user_id = current_user,
                que_id = info,
                user_type = user_type,
                rang = value + 1,
                phone = request.POST.get('phone'),)

                booking.save()
                msg = 'Successfully'
                context = {
                'info' : info,
                'msg' : msg
                    }
                return render(request, template_name='create_booking.html', context=context)

            if (qb != 0) and (w != 0):
                q_w = Que_walkin.objects.all().aggregate(Max('rang')).get('rang__max')
                q_b = Que_booking.objects.all().aggregate(Max('rang')).get('rang__max')

                if q_b >= q_w:
                    value = q_b
                else:
                    value = q_w

                booking = Que_booking.objects.create(
                user_id = current_user,
                que_id = info,
                user_type = user_type,
                rang = value + 1,
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
    que = QueInfo.objects.all()
    book_wait = Que_booking.objects.filter(status=1)
    walk_wait = Que_walkin.objects.filter(status=1)
    thisdict = {}
    count = 0
    for i in que:
            for j in book_wait:
                if j.que_id.id == i.id:
                    filter_qb = Que_booking.objects.filter(que_id=i.id,status=1)
                    my_book = Que_booking.objects.filter(que_id=i.id, status=1, user_id=current_user)
                    for f_qb in filter_qb:
                        for myq in my_book:
                            if f_qb.rang < myq.rang:
                                count += 1
                            else:
                                count += 0

                    filter_qw = Que_walkin.objects.filter(que_id=i.id,status=1)

                    for f_qw in filter_qw:
                        for myq in my_book:
                            if f_qw.rang < myq.rang:
                                count += 1
                            else:
                                count += 0
                    txt = i.id
                    thisdict[txt] = count
                    count = 0
        
            for k in walk_wait:
                if  k.que_id.id == i.id:
                    filter_qb = Que_booking.objects.filter(que_id=i.id,status=1)
                    my_book = Que_booking.objects.filter(que_id=i.id, status=1, user_id=current_user)

                    for f_qb in filter_qb:
                        for myq in my_book:
                            if f_qb.rang < myq.rang:
                                count += 1
                            else:
                                count += 0

                    filter_qw = Que_walkin.objects.filter(que_id=i.id,status=1)
                    for f_qw in filter_qw:
                        for myq in my_book:
                            if f_qw.rang < myq.rang:
                                count += 1
                            else:
                                count += 0
                    txt = i.id
                    thisdict[txt] = count
                    count = 0


    context = {'my_list' : my_list, 'thisdict': thisdict}
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
    q_w = Que_walkin.objects.all().aggregate(Max('rang')).get('rang__max')
    q_b = Que_booking.objects.all().aggregate(Max('rang')).get('rang__max')
    
    if q_b >= q_w:
        value = q_b
    else:
        value = q_w

    que_book.rang = value + 1 
    que_book.save()
    return redirect('my_booking')    



@user_passes_test(lambda u: u.is_authenticated)
@login_required
def my_history(request):
    current_user = request.user
    history = Que_booking.objects.filter(status=5,user_id=current_user)
    history_cel = Que_booking.objects.filter(status=2,user_id=current_user)
    history_del = Que_booking.objects.filter(status=3,user_id=current_user)
    context = {'history' : history, 'history_cel' : history_cel, 'history_del':history_del}

    return render(request, template_name='my_history.html', context=context)
   