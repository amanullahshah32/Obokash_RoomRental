from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
# from .forms import SignUpForm
from django.template import loader
from user.models import *
from datetime import *
import re
import os
from django.contrib import messages




def home(request):
    template = loader.get_template('home.html')
    context = {}
    context.update({'result': ''})
    context.update({'msg': 'Search your query'})
    return HttpResponse(template.render(context, request))


def contact(request):

    template = loader.get_template('contact.html')
    context = {}

    if request.method == 'POST':
        subject = request.POST['subject']
        email = request.POST['email']
        body = request.POST['body']
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if re.search(regex, email):
            pass
        else:
            template = loader.get_template('register.html')
            context.update({'msg': 'invalid email'})
            return HttpResponse(template.render(context, request))
        contact = Contact(subject=subject, email=email, body=body)
        contact.save()
        context.update({'msg': 'msg send to admin'})
        return HttpResponse(template.render(context, request))
    else:
        context.update({'msg': ''})
        return HttpResponse(template.render(context, request))
    

@login_required(login_url='/login')
def post(request):
    if request.method == "GET":
        context = {'user': request.user}
        return render(request, 'post.html', context)
    elif request.method == "POST":
        try:
            dimention = request.POST['dimention']
            location = request.POST['location'].lower()
            city = request.POST['city'].lower()
            state = request.POST['state'].lower()
            cost = request.POST['cost']
            hall = request.POST['hall'].lower()
            kitchen = request.POST['kitchen'].lower()
            balcany = request.POST['balcany'].lower()
            bedroom = request.POST['bedroom']
            ac = request.POST['AC'].lower()
            desc = request.POST['desc'].upper()
            img = request.FILES['img']
            user_obj = User.objects.filter(email=request.user.email)[0]
            bedroom = int(bedroom)
            cost = int(cost)
            room = Room.objects.create(
                user_email=user_obj,
                dimention=dimention,
                location=location,
                city=city,
                state=state,
                cost=cost,
                hall=hall,
                kitchen=kitchen,
                balcany=balcany,
                bedrooms=bedroom,
                AC=ac,
                desc=desc,
                img=img,
            )
            messages.success(request, 'submitted successfully..')
            return render(request, 'post.html')
        except Exception as e:
            return HttpResponse(status=500)


@login_required(login_url='/login')
def posth(request):
    if request.method == "GET":
        context = {'user': request.user}
        return render(request, 'posth.html', context)
    else:
        try:
            area = request.POST['area']
            floor = request.POST['floor']
            location = request.POST['location'].lower()
            city = request.POST['city'].lower()
            state = request.POST['state'].lower()
            cost = request.POST['cost']
            hall = request.POST['hall'].lower()
            kitchen = request.POST['kitchen'].lower()
            balcany = request.POST['balcany'].lower()
            bedroom = request.POST['bedroom']
            ac = request.POST['AC'].lower()
            desc = request.POST['desc'].upper()
            img = request.FILES['img']
            bedroom = int(bedroom)
            cost = int(cost)
            user_obj = User.objects.filter(email=request.user.email)[0]
            house = House.objects.create(
                user_email=user_obj,
                location=location,
                city=city,
                state=state,
                cost=cost,
                hall=hall,
                kitchen=kitchen,
                balcany=balcany,
                bedrooms=bedroom,
                area=area,
                floor=floor,
                AC=ac,
                desc=desc,
                img=img,
            )
            messages.success(request, 'submitted successfully..')
            return render(request, 'posth.html')
        except Exception as e:
            print()
            print(e)
            print()
            return HttpResponse(status=500)
