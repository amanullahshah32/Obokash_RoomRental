from urllib import request
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
from user.models import *  # Import relevant models
from datetime import *
import re
import os
from django.contrib import messages

# View for handling user login
def login_view(request):
    """
    This function handles user login requests.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object.
    """
    if request.method == 'GET':
        return render(request, 'login.html')

    email = request.POST['email']
    password = request.POST['password']
    user = authenticate(request, email=email, password=password)

    if user is not None:
        login(request, user)
        return redirect("/")
    else:
        template = loader.get_template('login.html')
        context = {
            'msg': 'Email and password you entered did not match.'
        }
        return HttpResponse(template.render(context, request))

# View for searching houses and rooms
def search(request):
    """
    This function handles search queries for houses and apartments.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object.
    """
    template = loader.get_template('home.html')
    context = {}
    if request.method == 'GET':
        typ = request.GET['type']  # Get the property type (House or Apartment)
        q = request.GET['q']  # Get the search query
        context.update({'type': typ})
        context.update({'q': q})
        results = {}

        if typ == 'House' and (bool(House.objects.filter(location=q)) or bool(House.objects.filter(city=q))):
            results = House.objects.filter(location=q)
            results = results | House.objects.filter(city=q)
        elif typ == 'Apartment' and (bool(Room.objects.filter(location=q)) or bool(House.objects.filter(city=q))):
            results = Room.objects.filter(location=q)
            results = results | Room.objects.filter(city=q)

        if not bool(results):
            messages.success(request, "No matching results for your query.")

        result = [results, len(results)]
        context.update({'result': result})

    return HttpResponse(template.render(context, request))


# View for registaring users
def register(request):
    """
    This function handles user registration requests.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object.
    """
    if request.method == 'GET':
        return render(request, 'register.html', {'msg': ''})

    name = request.POST['name']
    email = request.POST['email']
    location = request.POST['location']
    city = request.POST['city']
    phone = request.POST['phone']
    pas = request.POST['pass']
    cpas = request.POST['cpass']
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if re.search(regex, email):
        pass
    else:
        template = loader.get_template('register.html')
        context = {'msg': 'invalid email'}
        return HttpResponse(template.render(context, request))

    if len(str(phone)) != 11:
        template = loader.get_template('register.html')
        context = {'msg': 'invalid phone number'}
        return HttpResponse(template.render(context, request))

    if pas != cpas:
        template = loader.get_template('register.html')
        context = {'msg': 'password did not matched'}
        return HttpResponse(template.render(context, request))
    already = User.objects.filter(email=email)
    if bool(already):
        template = loader.get_template('register.html')
        context = {'msg': 'email already registered'}
        return HttpResponse(template.render(context, request))
    
    user = User.objects.create_user(
        name=name,
        email=email,
        location=location,
        city=city,
        number=phone,
        password=pas,
        )
    user.save()
    login(request, user)
    return redirect("/profile/")