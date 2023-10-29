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


def about(request):
    """
    Handles requests to display information about the website.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object.
    """
    template = loader.get_template('about.html')
    context = {}

    room = Room.objects.all()
    if bool(room):
        context.update({'room': room})
    house = House.objects.all()
    if bool(house):
        context.update({'house': house})
    return HttpResponse(template.render(context, request))


def home(request):
    """
    Handles the homepage view, providing the search functionality.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object.
    """
    template = loader.get_template('home.html')
    context = {}
    context.update({'result': ''})
    context.update({'msg': 'Search your query'})
    return HttpResponse(template.render(context, request))


def review(request):
    """
    Handles user reviews and contact requests.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object.
    """

    template = loader.get_template('review.html')
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
        review = Review(subject=subject, email=email, body=body)
        review.save()
        context.update({'msg': 'msg send to admin'})
        return HttpResponse(template.render(context, request))
    else:
        context.update({'msg': ''})
        return HttpResponse(template.render(context, request))
    

def recommendation(request):
    """
    Renders the recommendation page.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object.
    """
    return render(request, 'recommendation.html')

@login_required(login_url='/login')
def post(request):
    """
    Handles user's posting of room/apartment details.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object.
    """
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
    """
    Handles user's posting of house details.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object.
    """
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


def descr(request):
    """
    Renders the details of a house or apartment.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object.
    """
    template = loader.get_template('desc.html')
    context = {}
    if request.method == 'GET':
        id = request.GET['id']
        try:
            room = Room.objects.get(room_id=id)
            context.update({'val': room})
            context.update({'type': 'Apartment'})
            user = User.objects.get(email=room.user_email)
        except:
            house = House.objects.get(house_id=id)
            context.update({'val': house})
            context.update({'type': 'House'})
            user = User.objects.get(email=house.user_email)
    context.update({'user': user})
    return HttpResponse(template.render(context, request))

@login_required(login_url='/login')
def profile(request):
    """
    Renders the user profile page, displaying user details, posted rooms and houses, and contact reports.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object.
    """
    report = Review.objects.filter(email=request.user.email)
    room = Room.objects.filter(user_email=request.user)
    house = House.objects.filter(user_email=request.user)
    roomcnt = room.count()
    housecnt = house.count()
    reportcnt = report.count()
    rooms = []  # Initialize rooms as an empty list
    houses = []  # Initialize houses as an empty list

    if bool(room):
        n = len(room)
        nslide = n // 3 + (n % 3 > 0)
        rooms = [room, range(1, nslide), n]
    if bool(house):
        n = len(house)
        nslide = n // 3 + (n % 3 > 0)
        houses = [house, range(1, nslide), n]

    context = {
        'user': request.user,
        'report': report,
        'reportno': reportcnt,
        'roomno': roomcnt,
        'houseno': housecnt,
        'room': rooms,  # Assign rooms to context
        'house': houses,  # Assign houses to context
    }

    return render(request, 'profile.html', context=context)



def index(request):
    """
    Renders the home page, displaying a list of rooms and houses.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object.
    """
    template = loader.get_template('index.html')
    context = {}

    room = Room.objects.all()
    if bool(room):
        n = len(room)
        nslide = n // 3 + (n % 3 > 0)
        rooms = [room, range(1, nslide), n]
        context.update({'room': rooms})
    house = House.objects.all()
    if bool(house):
        n = len(house)
        nslide = n // 3 + (n % 3 > 0)
        houses = [house, range(1, nslide), n]
        context.update({'house': houses})
    return HttpResponse(template.render(context, request))

def deleter(request):
    """
    Deletes an apartment listing based on the provided ID and redirects to the user's profile page.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponseRedirect: Redirects to the user's profile page after deleting the apartment listing.
    """
    if request.method == 'GET':
        id = request.GET['id']
        instance = Room.objects.get(room_id=id)
        instance.delete()
        messages.success(request, 'Appartment details deleted successfully..')
    return redirect('/profile')

def deleteh(request):
    """
    Deletes a house listing based on the provided ID and redirects to the user's profile page.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponseRedirect: Redirects to the user's profile page after deleting the house listing.
    """
    if request.method == 'GET':
        id = request.GET['id']
        instance = House.objects.get(house_id=id)
        instance.delete()
        messages.success(request, 'House details deleted successfully..')
    return redirect('/profile')