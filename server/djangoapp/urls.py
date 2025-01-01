# Uncomment the imports before you add the code
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'

urlpatterns = [
    # Path for registration
    path(route='register', view=views.registration, name='registration'),
    
    # Path for login
    path(route='login', view=views.login_user, name='login'),
    
    # Path for logout
    path(route='logout', view=views.logout_request, name='logout'),
    
    # Path for dealer reviews view
    path(
        route='reviews/dealer/<int:dealer_id>',
        view=views.get_dealer_reviews,
        name='get_dealer_reviews'
    ),
    
    # Path for dealer details
    path(
        route='dealer/<int:dealer_id>',
        view=views.get_dealer_details,
        name='dealer_details'
    ),
    
    # Path for adding a review
    path(route='add_review', view=views.add_review, name='add_review'),
    
    # Path for getting all dealerships
    path(route='get_dealers/', view=views.get_dealerships, name='get_dealers'),
    
    # Path for getting dealerships by state
    path(
        route='get_dealers/<str:state>',
        view=views.get_dealerships,
        name='get_dealers_by_state'
    ),
    
    # Path for getting cars
    path(route='get_cars', view=views.get_cars, name='getcars'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
