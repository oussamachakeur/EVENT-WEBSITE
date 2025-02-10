from django.shortcuts import render , HttpResponse  ,redirect
from datetime import datetime
import calendar
from calendar import HTMLCalendar
from django.http import HttpResponseRedirect
from .models import Event , Venue
from .forms import VenueForm , EventForm



def event_Form(request):
    submitted= False
    if request.method == 'POST':
        form=EventForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/Event_form?submitted')
    else :
         form = EventForm()
         if 'submitted' in request.GET :
             submitted= True
   
    return render(request , 'event/Event_form.html' , {'form':form , 'submitted': submitted})


def update_venue(request ,venue_id ):
    venue = Venue.objects.get(pk= venue_id)
    form=VenueForm(request.POST or None , instance=venue)
    if form.is_valid():
        form.save()
        return redirect("venues")
    return render(request, 'event/update_venue.html', {'venue': venue ,'form':form,})

def update_event(request ,event_id ):
    event = Event.objects.get(pk= event_id)
    form=EventForm(request.POST or None , instance=event)
    if form.is_valid():
        form.save()
        return redirect("venues")
    return render(request, 'event/update_event.html', {'event': event ,'form':form,})



def search_venue(request):
    if request.method =='POST':
        searched = request.POST['searched']
        venues= Venue.objects.filter(name__contains=searched)
        return render(request ,  'event/search_venue.html' , {'searched': searched , 'venues':venues})
    else:
        return render(request ,  'event/search_venue.html' , {})




def show_venue(request , venue_id):
    venue = Venue.objects.get(pk= venue_id)
    return render(request, 'event/show_venue.html', {'venue': venue})




def venue_l(request):
    venues = Venue.objects.all() 
    return render(request, 'event/venues.html', {'venue_list': venues})



def Venue_Form(request):
    submitted= False
    if request.method == 'POST':
        form=VenueForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/Venue_form?submitted')
    else :
         form = VenueForm()
         if 'submitted' in request.GET :
             submitted= True
   
    return render(request , 'event/Venue_form.html' , {'form':form , 'submitted': submitted})

def event_l(request):
    event_list = Event.objects.all()
    context={
        'event_list': event_list
    }
    return render(request , 'event/events.html' , context)




def homepage(request, year=None, month=None):
    name = 'oussama'

    if year is None or month is None:
        today = datetime.today()
        year = today.year
        month = today.strftime("%B")  # Get month name

    month = month.title()  # Capitalize first letter

    # Convert month name to number
    try:
        month_number = list(calendar.month_name).index(month)
    except ValueError:
        return HttpResponse("Invalid month name", status=400)  # Handle invalid month names

    # Create the calendar
    cal = HTMLCalendar().formatmonth(year, month_number)

    context = {
        'name': name,
        'month_number': month_number,
        'cal': cal,
        'year': year,
        'month': month,
    }
    return render(request, 'event/home.html', context)

