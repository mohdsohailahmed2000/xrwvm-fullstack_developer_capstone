# Required imports
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.csrf import csrf_exempt
from .models import CarMake, CarModel
from .restapis import get_request, analyze_review_sentiments, post_review
from .populate import initiate
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create your views here.

@csrf_exempt
def login_user(request):
    """Handle user login."""
    data = json.loads(request.body)
    username = data.get('userName')
    password = data.get('password')
    user = authenticate(username=username, password=password)

    if user:
        login(request, user)
        return JsonResponse({"userName": username, "status": "Authenticated"})
    return JsonResponse({"userName": username, "error": "Authentication failed"})

def logout_request(request):
    """Handle user logout."""
    logout(request)
    return JsonResponse({"userName": ""})

@csrf_exempt
def registration(request):
    """Handle user registration."""
    data = json.loads(request.body)
    username = data.get('userName')
    password = data.get('password')
    first_name = data.get('firstName')
    last_name = data.get('lastName')
    email = data.get('email')

    if User.objects.filter(username=username).exists():
        return JsonResponse({"userName": username, "error": "Already Registered"})
    
    user = User.objects.create_user(
        username=username,
        first_name=first_name,
        last_name=last_name,
        password=password,
        email=email
    )
    login(request, user)
    return JsonResponse({"userName": username, "status": "Authenticated"})

def get_dealerships(request, state="All"):
    """Retrieve dealerships."""
    endpoint = "/fetchDealers" if state == "All" else f"/fetchDealers/{state}"
    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})

def get_dealer_reviews(request, dealer_id):
    """Retrieve reviews for a specific dealer."""
    if not dealer_id:
        return JsonResponse({"status": 400, "message": "Bad Request"})

    endpoint = f"/fetchReviews/dealer/{dealer_id}"
    reviews = get_request(endpoint)
    for review in reviews:
        sentiment_response = analyze_review_sentiments(review.get('review', ''))
        review['sentiment'] = sentiment_response.get('sentiment', 'neutral')
    return JsonResponse({"status": 200, "reviews": reviews})

def get_dealer_details(request, dealer_id):
    """Retrieve details for a specific dealer."""
    if not dealer_id:
        return JsonResponse({"status": 400, "message": "Bad Request"})

    endpoint = f"/fetchDealer/{dealer_id}"
    dealership = get_request(endpoint)
    return JsonResponse({"status": 200, "dealer": dealership})

@csrf_exempt
def add_review(request):
    """Submit a new review."""
    if request.user.is_anonymous:
        return JsonResponse({"status": 403, "message": "Unauthorized"})
    
    data = json.loads(request.body)
    try:
        post_review(data)
        return JsonResponse({"status": 200})
    except Exception as e:
        logger.error(f"Error posting review: {e}")
        return JsonResponse({"status": 401, "message": "Error in posting review"})

def get_cars(request):
    """Retrieve car makes and models."""
    if CarMake.objects.count() == 0:
        initiate()

    car_models = CarModel.objects.select_related('car_make')
    cars = [{"CarModel": model.name, "CarMake": model.car_make.name} for model in car_models]
    return JsonResponse({"CarModels": cars})
