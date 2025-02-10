
from django.contrib import admin
from django.urls import path , include
from .views import homepage , event_l , Venue_Form , venue_l , show_venue,search_venue , update_venue , event_Form , update_event

urlpatterns = [
    path('<int:year>/<str:month>', homepage , name='homepage'),
    path('', homepage , name='homepage'),
    path('events' , event_l , name='events'),
    path('Venue_form/', Venue_Form, name='VenueForm'),
    path('venues' , venue_l , name='venues'),
    path('show_venue/<venue_id>' , show_venue , name='show_venue'),
    path('search_venue', search_venue , name='search_venue'),
    path('update_venue/<venue_id>' , update_venue , name='update_venue'),
    path('Event_form/', event_Form, name='EventForm'),
    path('update_event/<event_id>' , update_event , name='update_event'),
]
