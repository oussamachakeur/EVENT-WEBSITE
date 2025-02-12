
from django.contrib import admin
from django.urls import path , include
from . import views
urlpatterns = [
    path('<int:year>/<str:month>', views.homepage , name='homepage'),
    path('', views.homepage , name='homepage'),
    path('events' , views.event_l , name='events'),
    path('Venue_form/', views.Venue_Form, name='VenueForm'),
    path('venues' , views.venue_l , name='venues'),
    path('show_venue/<venue_id>' , views.show_venue , name='show_venue'),
    path('search_venue', views.search_venue , name='search_venue'),
    path('update_venue/<venue_id>' , views.update_venue , name='update_venue'),
    path('Event_form/', views.event_Form, name='EventForm'),
    path('update_event/<event_id>' , views.update_event , name='update_event'),
    path('delete_event/<event_id>' , views.delete_event , name='delete_event'),
    path('delete_venue/<venue_id>' , views.delete_venue , name='delete_venue'),
    path('venue_txt' , views.venue_txt , name='venue_txt'),
    path('venue_csv' , views.venue_csv , name='venue_csv'),
    path('venue_PDF' , views.venue_PDF , name='venue_PDF'),
    path('download_venues' , views.download_venues , name='download_venues'),
]


