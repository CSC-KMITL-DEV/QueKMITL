from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.context_processors import request
from .models import Department, QueInfo, TypeUser, Week_Day, TypeQue, Type_in_Dep
from booking.models import Que_booking, Que_walkin
from user.models import User_punish
from string import punctuation
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Max


# Create your views here.
@login_required
@user_passes_test(lambda s: s.is_staff)
def department(request):
    dep_all = Department.objects.all()
    context = {
        'dep_all' : dep_all
    }
    return render(request, template_name='department.html', context=context)

# Create your views here.
@login_required
@user_passes_test(lambda s: s.is_staff)
def create_dep(request):
    context = {}
    symbols = set(punctuation)

    msg = ''
    if request.method == 'POST':
        if any(c in symbols for c in request.POST.get('name_dep')):
            error = 'ต้องไม่มีตัวอักษรพิเศษในชื่อคิว !'
            context = {
            'error' : error,
            }
            return render(request, template_name='dep_form.html', context=context)
        else:
            dep = Department.objects.create(
            name_dep = request.POST.get('name_dep'),)
            dep.save()
            msg = 'Successfully'

            context = {
                'msg' : msg,
                }
            return render(request, template_name='dep_form.html', context=context)

    return render(request, template_name='dep_form.html')

@user_passes_test(lambda s: s.is_staff)
@login_required
def type_in_dep(request, id):
    dep = Department.objects.get(pk=id)
    t_in_dep = Type_in_Dep.objects.filter(dep_id=dep.id)
    context = {
        't_in_dep' : t_in_dep,
        'dep' : dep,
    }
    return render(request, template_name='type_in_dep.html', context=context)

@user_passes_test(lambda s: s.is_staff)
@login_required
def create_type_in_dep(request, id):
    dep = Department.objects.get(pk=id)
    context = {}
    symbols = set(punctuation)

    msg = ''
    if request.method == 'POST':
            t_dep = Type_in_Dep.objects.create(
            name_que_dep = request.POST.get('nametype_dep'),
            dep_id = dep)
            t_dep.save()
            msg = 'Successfully'
            context = {
                'msg' : msg,
                'dep' : dep,
                }
            return render(request, template_name='type_in_dep_form.html', context=context)

    context = {
        
        'dep' : dep,
    }
    return render(request, template_name='type_in_dep_form.html', context=context)

@user_passes_test(lambda s: s.is_staff)
@login_required
def view_que(request, id):
    tdep = Type_in_Dep.objects.get(pk=id)

    context = {}
    que_list = QueInfo.objects.filter(status=1, type_in_dep_id=tdep)
    que_list = que_list.order_by('date_start')
    context = {
        'que_list' : que_list,
        'tdep' : tdep,
        }
    return render(request, template_name='view_que.html', context=context)

@user_passes_test(lambda s: s.is_staff)
@login_required
def forms(request, id):
    dep_t = Type_in_Dep.objects.get(pk=id)
    context = {}
    msg = ''
    symbols = set(punctuation)

    list_user = TypeUser.objects.all()
    list_day = Week_Day.objects.all()
    list_que = TypeQue.objects.all()
    

    if request.method == 'POST':
        if any(c in symbols for c in request.POST.get('nameque')):
            sb_name = 'ต้องไม่มีตัวอักษรพิเศษในชื่อคิว !'
            context = {
            'sb_name' : sb_name,
            'list_user': list_user,
            'list_day' : list_day,
            'list_que' : list_que,
            'dep_t' : dep_t,
            }
            return render(request, template_name='forms.html', context=context)

        if (request.POST.get('timeeend') <= request.POST.get('timestart')):
            checkt = 'เวลาสิ้นสุดไม่สามารถเลือกก่อน หรือ เท่ากับเวลาเริ่มต้นได้ !'
            context = {
            'checkt' : checkt,
            'list_user': list_user,
            'list_day' : list_day,
            'list_que' : list_que,
            'dep_t' : dep_t,
            }
            return render(request, template_name='forms.html', context=context)

        if request.POST.get('dateend') < request.POST.get('datestart'):
            checkd = 'วันเริ่มต้นต้องเลือกก่อนวันสิ้นสุด และ วันสิ้นสุดไม่สามารถเลือกก่อนวันเริ่มต้นได้ !'
            context = {
            'checkd' : checkd,
            'list_user': list_user,
            'list_day' : list_day,
            'list_que' : list_que,
            'dep_t' : dep_t,
            }
            return render(request, template_name='forms.html', context=context)


            # เช็คตัวอักษรเดียว
        if len(request.POST.get('prefix')) > 1:
            checkp = 'ต้องใส่เพียงหนึ่งตัวอักษร !'
            context = {
            'checkp' : checkp,
            'list_user': list_user,
            'list_day' : list_day,
            'list_que' : list_que,
            'dep_t' : dep_t,
            }
            return render(request, template_name='forms.html', context=context)


            # เช็คตัวเลข
        if request.POST.get('prefix').isnumeric() == True:
            pfnum = 'ต้องใส่เป็นตัวอักษร ห้ามเป็นตัวเลข !'
            context = {
            'pfnum' : pfnum,
            'list_user': list_user,
            'list_day' : list_day,
            'list_que' : list_que,
            'dep_t' : dep_t,
            }
            return render(request, template_name='forms.html', context=context)

            # เช็คตัวอักษรพิเศษ
        if (any(c in symbols for c in request.POST.get('prefix'))):
            sb_prefix = 'ต้องไม่มีตัวอักษรพิเศษใน Prefix !'
            context = {
            'sb_prefix' : sb_prefix,
            'list_user': list_user,
            'list_day' : list_day,
            'list_que' : list_que,
            'dep_t' : dep_t,
            }
            return render(request, template_name='forms.html', context=context)

        # เช็ค prefix ซ้ำ
        if request.POST.get('prefix') :
            prefix_upper = request.POST.get('prefix').upper()
            prefix_filter = QueInfo.objects.filter(prefix=prefix_upper)
            for p in prefix_filter:
                if p.status == True:
                    pf = 'ตัวอักษรนี้มีการใช้งานแล้ว !'

                    context = {
                    'pf' : pf,
                    'list_user': list_user,
                    'list_day' : list_day,
                    'list_que' : list_que,
                    'dep_t' : dep_t,
                    }
                    return render(request, template_name='forms.html', context=context)
                else:
                    pass
            else:
                pass

        if not request.POST.getlist('daySelector'):
            openday = 'ต้องกำหนดวันเปิดทำการ !'
            context = {
            'openday' : openday,
            'list_user': list_user,
            'list_day' : list_day,
            'list_que' : list_que,
            'dep_t' : dep_t,
            }
            return render(request, template_name='forms.html', context=context)

        if not request.POST.getlist('typeque'):
            typeque = 'ต้องใส่รูปแบบการบริการ !'
            context = {
            'typeque' : typeque,
            'list_user': list_user,
            'list_day' : list_day,
            'list_que' : list_que,
            'dep_t' : dep_t,
            }
            return render(request, template_name='forms.html', context=context)

        if not request.POST.getlist('typeuser'):
            typeuser = 'ต้องกำหนดบุคคลรับบริการ !'
            context = {
            'typeuser' : typeuser,
            'list_user': list_user,
            'list_day' : list_day,
            'list_que' : list_que,
            'dep_t' : dep_t,
            }
            return render(request, template_name='forms.html', context=context)


        # เช็คข้อมูลผ่านทั้งหมด

        que_info = QueInfo.objects.create(
        name_que = request.POST.get('nameque'),
        prefix = request.POST.get('prefix').upper(),
        date_start = request.POST.get('datestart'),
        date_end = request.POST.get('dateend'),
        time_start = (request.POST.get('timestart')),
        time_end = (request.POST.get('timeeend')),
        wait_time = request.POST.get('waittime'),
        type_in_dep_id = dep_t)

        for d in request.POST.getlist('daySelector'):
            que_info.day_open.add(d)

        for q in request.POST.getlist('typeque'):
            que_info.type_que.add(q)

        for u in request.POST.getlist('typeuser'):
            que_info.type_user.add(u)

        que_info.save()
        msg = 'Successfully'
        context = {
        'msg' : msg,
            'list_user': list_user,
            'list_day' : list_day,
            'list_que' : list_que,
            'dep_t' : dep_t,
        }
        return render(request, template_name='forms.html', context=context)

    else:
        que_info = QueInfo.objects.none()

    context = {
            'list_user': list_user,
            'list_day' : list_day,
            'list_que' : list_que,
            'dep_t' : dep_t,
            }
    return render(request, template_name='forms.html', context=context)


@user_passes_test(lambda s: s.is_staff)
@login_required
def info_que(request, id):
    context = {}
    info = QueInfo.objects.get(pk=id)
    day = info.day_open.all()
    typeque = info.type_que.all()
    typeuser = info.type_user.all()
    using_status = Que_booking.objects.filter(que_id=id,status=5)
    booking_before = Que_booking.objects.filter(que_id=id,status=1).order_by('rang')
    sum_bf = booking_before.count()
    time_wait_walkin = sum_bf
    booking_walkin = Que_walkin.objects.filter(que_id=id,status=1).order_by('rang')
    using_walkin = Que_walkin.objects.filter(que_id=id,status=3)
    context = {
        'info' : info,
        'day' : day,
        'typeque' : typeque,
        'typeuser' : typeuser,  
        'booking_before' : booking_before,
        'booking_walkin' : booking_walkin,
        'using_status' : using_status,
        'sum_bf' : sum_bf,
        'time_wait_walkin' : time_wait_walkin,
        'using_walkin' : using_walkin,
        }
    return render(request, template_name='que_info.html', context=context)



@user_passes_test(lambda s: s.is_staff)
@login_required
def close_que(request, id):
    context = {}
    que = QueInfo.objects.get(pk=id)
    que.status = 0
    que.save()
    return redirect('view_que',id=que.type_in_dep_id.id)

@user_passes_test(lambda s: s.is_staff)
@login_required
def success(request,id):
    que_book = Que_booking.objects.get(pk=id)
    que_book.status = 5
    que_book.save()

    return redirect("info_que", id=que_book.que_id.id)

@user_passes_test(lambda s: s.is_staff)
@login_required
def using(request,id):
    que_book = Que_booking.objects.get(pk=id)
    que_book.status = 4
    que_book.save()
    return redirect('info_que', id=que_book.que_id.id)


@user_passes_test(lambda s: s.is_staff)
@login_required
def putoff(request,id):
    que_book = Que_booking.objects.get(pk=id)
    q_w = Que_walkin.objects.all().aggregate(Max('rang')).get('rang__max')
    q_b = Que_booking.objects.all().aggregate(Max('rang')).get('rang__max')
    
    if q_b >= q_w:
        value = q_b
    else:
        value = q_w

    que_book.rang = value + 1 
    que_book.save()
    return redirect('info_que', id=que_book.que_id.id)    
    

@user_passes_test(lambda s: s.is_staff)
@login_required
def delete(request,id):
    que_book = Que_booking.objects.get(pk=id)
    que_book.status = 3
    que_book.save()
    return redirect('info_que', id=que_book.que_id.id)    
    
    
    
@user_passes_test(lambda s: s.is_staff)
@login_required
def cancel(request,id):
    que_book = Que_booking.objects.get(pk=id)
    que_book.status = 2
    que_book.save()
    punish = User_punish.objects.get(user=que_book.user_id)
    punish.punish += 1
    punish.save()
    return redirect('info_que', id=que_book.que_id.id)    


@user_passes_test(lambda s: s.is_staff)
@login_required
def success_walkin(request,id):
    que_walkin = Que_walkin.objects.get(pk=id)
    que_walkin.status = 4
    que_walkin.save()

    return redirect("info_que", id=que_walkin.que_id.id)

@user_passes_test(lambda s: s.is_staff)
@login_required
def using_walkin(request,id):
    que_walkin = Que_walkin.objects.get(pk=id)
    que_walkin.status = 3
    que_walkin.save()
    return redirect('info_que', id=que_walkin.que_id.id)


@user_passes_test(lambda s: s.is_staff)
@login_required
def delete_walkin(request,id):
    que_walkin = Que_walkin.objects.get(pk=id)
    que_walkin.status = 2
    que_walkin.save()
    return redirect('info_que', id=que_walkin.que_id.id)   



@user_passes_test(lambda s: s.is_staff)
@login_required
def userbook(request,id):
    info = QueInfo.objects.get(pk=id)
    booking_before = Que_booking.objects.filter(que_id=id,status=1)
    booking_putoff = Que_booking.objects.filter(que_id=id,status=2)
    walkin_que = Que_walkin.objects.filter(que_id=id,status=1)
    count_bf = booking_before.count()
    count_bp = booking_putoff.count()
    count_w = walkin_que.count()
    punish = User_punish.objects.all()
    context = {
        'info' : info,
        'booking_before' : booking_before,
        'booking_putoff' : booking_putoff,
        'walkin_que' : walkin_que,
        'count_bf' : count_bf,
        'count_bp' : count_bp,
        'count_w' : count_w,
        'punish' : punish
        }
    return render(request, template_name='userbook_queinfo.html', context=context)


@user_passes_test(lambda s: s.is_staff)
@login_required
def create_walkin(request,id):
    info = QueInfo.objects.get(pk=id)
    typeu = info.type_user.all()
    w = Que_walkin.objects.all().count()
    qb = Que_booking.objects.all().count()
    if request.method == 'POST':
        if (request.POST.get('phone').isnumeric() == True) and (len(request.POST.get('phone')) == 10):
            
            if (w == 0) and (qb == 0):
                que_walkin = Que_walkin.objects.create(
                name = request.POST.get('username'),
                user_type_id = request.POST.get('types_id'),
                phone = request.POST.get('phone'),
                rang = 1,
                que_id = info,)
                que_walkin.save()
                msg = 'Successfully'
                context = {
                'msg' : msg,
                'info' : info,
                'typeu' : typeu,
                }
                return render(request, template_name='create_walkin.html', context=context)

            if (w != 0) and (qb == 0):
                qw = Que_walkin.objects.aggregate(Max('rang')).get('rang__max')
                value = qw
                que_walkin = Que_walkin.objects.create(
                name = request.POST.get('username'),
                user_type_id = request.POST.get('types_id'),
                phone = request.POST.get('phone'),
                rang = value + 1,
                que_id = info,)
                que_walkin.save()
                msg = 'Successfully'
                context = {
                'msg' : msg,
                'info' : info,
                'typeu' : typeu,
                }
                return render(request, template_name='create_walkin.html', context=context)   

            if (qb != 0) and (w == 0):
                q = Que_booking.objects.aggregate(Max('rang')).get('rang__max')
                value = q
                que_walkin = Que_walkin.objects.create(
                name = request.POST.get('username'),
                user_type_id = request.POST.get('types_id'),
                phone = request.POST.get('phone'),
                rang = value + 1,
                que_id = info,)
                que_walkin.save()
                msg = 'Successfully'
                context = {
                'msg' : msg,
                'info' : info,
                'typeu' : typeu,
                }
                return render(request, template_name='create_walkin.html', context=context)               
                        
            if (qb != 0) and (w != 0):
                q_w = Que_walkin.objects.all().aggregate(Max('rang')).get('rang__max')
                q_b = Que_booking.objects.all().aggregate(Max('rang')).get('rang__max')

                if q_b >= q_w:
                    value = q_b
                else:
                    value = q_w

                que_walkin = Que_walkin.objects.create(
                name = request.POST.get('username'),
                user_type_id = request.POST.get('types_id'),
                phone = request.POST.get('phone'),
                rang = value + 1,
                que_id = info,)
                que_walkin.save()
                msg = 'Successfully'
                context = {
                'msg' : msg,
                'info' : info,
                'typeu' : typeu,
                }
                return render(request, template_name='create_walkin.html', context=context)
        else:
            error = 'กรุณาใส่เบอร์โทรศัพท์ให้ถูกต้อง'
            context = {
                'info' : info,
                'typeu' : typeu,
                'error' : error
                }
            return render(request, template_name='create_walkin.html', context=context)
    else:
        booking = Que_walkin.objects.none()
    context = {
        'info' : info,
        'typeu' : typeu,     
        }
    return render(request, template_name='create_walkin.html', context=context)




@user_passes_test(lambda s: s.is_staff)
@login_required
def show_que(request):
    book_que = Que_booking.objects.filter(status=5)
    walkin = Que_walkin.objects.filter(status=3)
    book_wait = Que_booking.objects.filter(status=1)
    walk_wait = Que_walkin.objects.filter(status=1)

    que = QueInfo.objects.all()
    thisdict =	{}
    count = 0
    for i in que:
        for j in book_wait:
            for k in walk_wait:
                if j.que_id.id == i.id or k.que_id.id == i.id:
                    count = Que_booking.objects.filter(que_id=i.id,status=1).count()
                    count += Que_walkin.objects.filter(que_id=i.id,status=1).count()
                    thisdict[i.name_que] = count
             

                
    


    context = {
        'book_que' : book_que,
        'walkin' : walkin,
        'book_wait' : book_wait,
        'walk_wait' : walk_wait,
        'que' : que,
        'thisdict' : thisdict,
        }
    return render(request, template_name='show_que.html', context=context)

