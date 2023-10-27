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