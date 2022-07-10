from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarMake, CarModel, CarDealer
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/index.html', context)
    else:
        return render(request, 'djangoapp/index.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        context = dict()

        url = "https://4eb88eae.eu-de.apigw.appdomain.cloud/api/dealership"
        context['dealerships'] = get_dealers_from_cf(url)

        return render(request, 'djangoapp/index.html', context)

# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        context = dict()

        url = "https://4eb88eae.eu-de.apigw.appdomain.cloud/api/review"
        # Get dealers from the URL
        context['reviews'] = get_dealer_reviews_from_cf(url = url, dealerId = dealer_id)
        context['dealerId'] = dealer_id

        # Concat all dealer's short name
        if 'status' in context['reviews']:
            return HttpResponse(404)

        return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
def add_review(request, dealer_id):
    user = request.user

    # if request.method == "POST" and user.is_authenticated:
    if request.method == "GET":
        context = dict()
        context['dealerId'] = dealer_id
        # dealer name missing
        url = "https://4eb88eae.eu-de.apigw.appdomain.cloud/api/dealership"
        dealerships = get_dealers_from_cf(url)

       
        for dealer in dealerships:
            if dealer.id == dealer_id:
                dealer_name = dealer.full_name
                break

        context['dealer_name'] = dealer_name
        # print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        # print(dealer_name)
        # print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

        # get car models
        cars = CarModel.objects.all().filter(dealerId=dealer_id)
        # error when empty...
        # print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        # print(cars)
        # print(cars[0].carMake.name)
        # print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        

        context['cars'] = cars
        # context('dealer_name')

        return render(request, 'djangoapp/add_review.html', context)
    elif request.method == "POST":
        url = 'https://4eb88eae.eu-de.apigw.appdomain.cloud/api/review'

        # >>>>>>>>>>>>>>
        # print(request.POST['content'])
        # print(request.POST['purchasecheck'])
        # print(request.POST['car'])
        # carmodel = CarModel.objects.all().filter(id = request.POST['car'])
        # print(carmodel[0].name)
        # print(carmodel[0].carMake.name)
        # print(carmodel[0].year)
        # print(request.POST['purchasedate'])
        # print("~~")
        # print(dealer_id)
        # print("~~")
        # print(user.first_name + ' ' + user.last_name)
        # print( request.POST['purchasedate'] )
        # return False

        review = dict()
        review['name'] = user.first_name + ' ' + user.last_name
        review["dealership"] = dealer_id
        review["review"] = request.POST['content']

        purchasecheck = request.POST.get('purchasecheck', False) 
        if purchasecheck == "on":
            purchasecheck = True
        review["purchase"] = purchasecheck
        
        if purchasecheck == True and request.POST['car'] != '':
            carmodel = CarModel.objects.all().filter(id = request.POST['car'])
            review["purchase_date"] = request.POST['purchasedate']
            review["car_make"] = carmodel[0].carMake.name
            review["car_model"] = carmodel[0].name
            review["car_year"] = carmodel[0].year.strftime("%Y")

        json_payload = dict()
        json_payload["review"] = review

        response = post_request(url, json_payload, dealerId=dealer_id)
        return HttpResponse(response)
    else:
        return HttpResponse("nope")
