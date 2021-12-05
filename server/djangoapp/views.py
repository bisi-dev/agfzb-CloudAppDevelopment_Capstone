from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect, get_list_or_404
from .models import CarMake, CarModel
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
from .restapis import get_dealers_from_cf, get_dealer_by_state_from_cf, get_dealer_reviews_from_cf, post_request, get_dealer_by_id_from_cf

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
    # Handles POST request
    if request.method == "POST":
        # Get username and password from request.POST dictionary
        username = request.POST['username']
        password = request.POST['psw']
        # Try to check if provide credential can be authenticated
        user = authenticate(username=username, password=password)
        if user is not None:
            # If user is valid, call login method to login current user
            login(request, user)
            return redirect('djangoapp:index')
        else:
            # If not, return to login page again
            return render(request, 'djangoapp/user_login.html', context)
    else:
        return render(request, 'djangoapp/user_login.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    context = {}
    return render(request, 'djangoapp/user_logout.html', context)

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    # If it is a GET request, just render the registration page
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    # If it is a POST request
    elif request.method == 'POST':
        # Get user information from request.POST
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            # Check if user already exists
            User.objects.get(username=username)
            user_exist = True
        except:
            # If not, simply log this is a new user
            logger.debug("{} is new user".format(username))
        # If it is a new user
        if not user_exist:
            # Create user in auth_user table
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            # Login the user and redirect to course list page
            login(request, user)
            return redirect("djangoapp:index")
        else:
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = "https://aa2f598f.eu-gb.apigw.appdomain.cloud/api/dealership"
        dealerships = get_dealers_from_cf(url)
        context["dealership_list"] = dealerships
        #dealerships = get_dealer_by_state_from_cf(url,'TX')
        #dealer_names = ' '.join([dealer.short_name+" - " for dealer in dealerships])
        #return HttpResponse(dealer_names)
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    context = {}
    context["id"] = dealer_id

    if request.method == "GET":
        url_review = "https://aa2f598f.eu-gb.apigw.appdomain.cloud/api/review"
        url_dealer = "https://aa2f598f.eu-gb.apigw.appdomain.cloud/api/dealership"
        reviews = get_dealer_reviews_from_cf(url_review, dealer_id)
        dealer = get_dealer_by_id_from_cf (url_dealer, dealer_id)

        context["reviews_list"] = reviews
        context["dealer"] = dealer[0]

        return render(request, 'djangoapp/dealer_details.html', context)   


# Create a `add_review` view to submit a review
def add_review(request, dealer_id):

    if request.method == "POST":

        print("-------------------------------------------------------------------------1")
        print(request.POST["purchasedate"])
        print(request.POST["content"])

        if ("purchasecheck" in request.POST):
            print(request.POST["purchasecheck"])
            purchase_check = True
        else:
            print("No purchasecheck")
            purchase_check = False

        print(dealer_id)
        url_dealer = "https://aa2f598f.eu-gb.apigw.appdomain.cloud/api/dealership"
        dealer = get_dealer_by_id_from_cf (url_dealer, dealer_id)   
        print(dealer[0].full_name)

        carmodel = get_object_or_404(CarModel, pk=request.POST["car"])
        print(carmodel.name)
        print(carmodel.carmake.name)
        print(carmodel.year.strftime("%Y"))
        print(request.user.first_name+" "+request.user.last_name)
        print("-------------------------------------------------------------------------")

        if request.user.is_authenticated:
            review = dict()
            review["time"] = datetime.utcnow().isoformat()
            review["dealership"] = dealer_id
            review["review"] = request.POST["content"]

            review["name"] = request.user.first_name+" "+request.user.last_name
            review["purchase"] = purchase_check
            review["purchase_date"] = request.POST["purchasedate"]
            review["car_make"] = carmodel.carmake.name   
            review["car_model"] = carmodel.name
            review["car_year"] = carmodel.year.strftime("%Y")

            json_payload = dict()
            json_payload["review"] = review

            url = "https://aa2f598f.eu-gb.apigw.appdomain.cloud/api/review"

            result = ""
            print("-------------------------------------------------------------------------2")
            print(review)
            print("-------------------------------------------------------------------------")
            result =  post_request(url, json_payload)
            print(result)

            print("-------------------------------------------------------------------------<<<<<<<<<<<<<<<<<<<<<<")
            return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
        else:
            print("Not autenticated")
            return HttpResponse("User not authenticated")

    elif request.method == "GET":
        context = {}

        url_dealer = "https://aa2f598f.eu-gb.apigw.appdomain.cloud/api/dealership"
        dealer = get_dealer_by_id_from_cf (url_dealer, dealer_id)

        context["dealer"] = dealer[0]        
        context["dealer_id"] = dealer_id

        #Get cars
        #cars = get_list_or_404(CarModel, dealer_id=dealer_id)

        cars = list(CarModel.objects.filter(dealer_id=dealer_id))

        context["cars"] = cars
        if not cars:
            context["cars_found"] = False
        else:
            context["cars_found"] = True

        return render(request, 'djangoapp/add_review.html', context)  