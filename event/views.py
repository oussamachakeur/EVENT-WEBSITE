from django.shortcuts import render , HttpResponse  ,redirect
from datetime import datetime
import calendar
from calendar import HTMLCalendar
from django.http import HttpResponseRedirect , HttpResponse
from .models import Event , Venue
from .forms import VenueForm , EventForm
import csv

# PDF stuff 
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import LETTER

#pagination stuff 
from  django.core.paginator import Paginator


def download_venues(request):
    return render(request, 'event/download_venues.html')


def venue_PDF(request):
    # create a bytestream buffer 
    buf = io.BytesIO()
    # create cavas 
    c = canvas.Canvas(buf , pagesize= LETTER , bottomup=0)
    #create a text object
    textop = c.beginText()
    textop.setTextOrigin(inch , inch)
    textop.setFont("Helvetica" , 14 )

    venues= Venue.objects.all()
    lines =[]

    for venue in venues:

        lines.append(venue.name)
        lines.append(venue.address)
        lines.append(venue.zip_code)
        lines.append(venue.email)
        lines.append("")
        lines.append("")
        lines.append("")


    for line in lines:
        textop.textLine(line)

    c.drawText(textop)
    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf , as_attachment=True , filename="Venue.PDF")

def venue_csv(request):
    response = HttpResponse(content_type = 'text/csv')
    response['Content-Disposition'] = 'attachment; filename= Venues.csv'
    writer = csv.writer(response)
    venues= Venue.objects.all()
    writer.writerow(['name','address','zip_code','phone','email'])

    for venue in venues:
        writer.writerow([venue.name , venue.address , venue.zip_code , venue.phone , venue.email])
    return response



def venue_txt(request):
    response = HttpResponse(content_type = 'text/plain')
    response['Content-Disposition'] = 'attachment; filename= Venues.txt'
    venues= Venue.objects.all()
    lines=[]
    for venue in venues:
        lines.append(f'{venue.name}\n {venue.address}\n {venue.zip_code}\n {venue.phone}\n {venue.email}\n\n\n\n\n')
    #lines=['hi hihih ih ih ih i']
    response.writelines(lines)
    return response


def delete_event(request , event_id):
    event = Event.objects.get(pk= event_id)
    event.delete()
    return redirect('/events')

def delete_venue(request , venue_id):
    event = Venue.objects.get(pk= venue_id)
    event.delete()
    return redirect('/venues')


def event_Form(request):
    submitted= False
    if request.method == 'POST':
        form=EventForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/events?submitted')
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
    #venues = Venue.objects.all().order_by('name')

   #pagination 
    p= Paginator(Venue.objects.all() , 2)
    page = request.GET.get('page')
    venues= p.get_page(page)

    return render(request, 'event/venues.html', {'venues': venues})



def Venue_Form(request):
    submitted= False
    if request.method == 'POST':
        form=VenueForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/venues?submitted')
    else :
         form = VenueForm()
         if 'submitted' in request.GET :
             submitted= True
   
    return render(request , 'event/Venue_form.html' , {'form':form , 'submitted': submitted})

def event_l(request):
    #event_list = Event.objects.all().order_by('name')

    p = Paginator(Event.objects.all() , 2)
    page = request.GET.get('page')
    events = p.get_page(page)

    context={
        'events': events
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

