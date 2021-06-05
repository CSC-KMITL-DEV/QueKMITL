from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.context_processors import request
from .models import QueInfo, TypeUser, Week_Day, TypeQue
from string import punctuation
# Create your views here.

def forms(request):
    
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
            }
            return render(request, template_name='forms.html', context=context)

        if (request.POST.get('timeeend') <= request.POST.get('timestart')):
            checkt = 'เวลาสิ้นสุดไม่สามารถเลือกก่อน หรือ เท่ากับเวลาเริ่มต้นได้ !'
            context = {
            'checkt' : checkt,
            'list_user': list_user,
            'list_day' : list_day,
            'list_que' : list_que,
            }
            return render(request, template_name='forms.html', context=context)

        if request.POST.get('dateend') < request.POST.get('datestart'):
            checkd = 'วันเริ่มต้นต้องเลือกก่อนวันสิ้นสุด และ วันสิ้นสุดไม่สามารถเลือกก่อนวันเริ่มต้นได้ !'
            context = {
            'checkd' : checkd,
            'list_user': list_user,
            'list_day' : list_day,
            'list_que' : list_que,
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
            }
            return render(request, template_name='forms.html', context=context)

        if not request.POST.getlist('typeque'):
            typeque = 'ต้องใส่รูปแบบการบริการ !'
            context = {
            'typeque' : typeque,
            'list_user': list_user,
            'list_day' : list_day,
            'list_que' : list_que,
            }
            return render(request, template_name='forms.html', context=context)

        if not request.POST.getlist('typeuser'):
            typeuser = 'ต้องกำหนดบุคคลรับบริการ !'
            context = {
            'typeuser' : typeuser,
            'list_user': list_user,
            'list_day' : list_day,
            'list_que' : list_que,
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
        wait_time = request.POST.get('waittime'),)

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
        }
        return render(request, template_name='forms.html', context=context)

    else:
        que_info = QueInfo.objects.none()

    context = {
            'list_user': list_user,
            'list_day' : list_day,
            'list_que' : list_que,
            }
    return render(request, template_name='forms.html', context=context)

def view_que(request):
    context = {}
    que_list = QueInfo.objects.filter(status=1)
    que_list = que_list.order_by('date_start')

    context = {
        'que_list' : que_list,
        }
    return render(request, template_name='view_que.html', context=context)


def info_que(request, id):
    context = {}
    info = QueInfo.objects.get(pk=id)

    context = {
        'info' : info,
        }
    return render(request, template_name='que_info.html', context=context)

