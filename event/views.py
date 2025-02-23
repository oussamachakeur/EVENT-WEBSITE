from django.shortcuts import render , HttpResponse  ,redirect
from datetime import datetime
import calendar
from calendar import HTMLCalendar
from django.http import HttpResponseRedirect , HttpResponse
from .models import Event , Venue
## import user model 
from django.contrib.auth.models import User

from .forms import VenueForm , EventForm ,EventFormAdmin
import csv
from django.contrib import messages

# PDF stuff 
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import LETTER

#pagination stuff 
from  django.core.paginator import Paginator




def admin_approval(request):
    events_count= Event.objects.all().count()
    venue_count= Venue.objects.all().count()
    users_count = User.objects.all().count()
    events= Event.objects.all()
    if request.user.is_superuser:
        if request.method =='POST':
        
            id_list = request.POST.getlist('boxes')
            events.update(approved=False)
            for x in id_list:
                Event.objects.filter(pk=int(x)).update(approved = True)

            return redirect('events')
        else:
            return render(request , 'event/admin_approval.html' , {
                'events':events,
                'events_count':events_count,
                'venue_count':venue_count,
                'users_count':users_count,
                })
    else : 
        messages.error(request , (' you are not authorized '))
        return redirect('events')
    
    return render(request , 'event/admin_approval.html' , {'events':events})

def myEvent(request):
    if request.user.is_authenticated:
        me = request.user.id
        events = Event.objects.filter(manager= me)  
        
        #print(events)  
        return render(request, 'event/myEvent.html', {"events": events})

    else:
        messages.error(request, 'You are not authorized')
        return redirect('home')



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
    if request.user == event.manager:
        messages.success(request , 'it has been deleted succesfully')
        event.delete()
        return redirect('/events')
    else : 
        messages.error(request , 'user is not authorized to delete this .')
        return redirect('/events')

def delete_venue(request , venue_id):
    event = Venue.objects.get(pk= venue_id)
    event.delete()
    return redirect('/venues')


def event_Form(request):
    submitted= False
    if request.method == 'POST':
        if request.user.is_superuser:   # this mean id of superuser in django , if iwant someone else i can make it like request.user.id == 2 for ex.
            form=EventFormAdmin(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/events?submitted')
        else:
            form=EventForm(request.POST)
            if form.is_valid():
                event = form.save(commit=False)
                event.manager = request.user
                event.save()
                return HttpResponseRedirect('/events?submitted')
    else:
        if request.user.is_superuser:
            form = EventFormAdmin
        else :   
            form = EventForm

            if 'submitted' in request.GET:
                submitted= True
   
    return render(request , 'event/Event_form.html' , {'form':form , 'submitted': submitted})


def update_venue(request ,venue_id ):
    venue = Venue.objects.get(pk= venue_id)
    form=VenueForm(request.POST or None ,request.FILES or None , instance=venue)
    if form.is_valid():
        form.save()
        return redirect("venues")
    return render(request, 'event/update_venue.html', {'venue': venue ,'form':form,})

def update_event(request ,event_id ):
    event = Event.objects.get(pk= event_id)
    if request.user.is_superuser:
        form=EventFormAdmin(request.POST or None , instance=event)
    else: 
        form=EventFormAdmin(request.POST or None , instance=event)

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
    venueOwner= User.objects.get(pk=venue.owner)
    return render(request, 'event/show_venue.html', {'venue': venue , 'venueOwner': venueOwner})




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
        form=VenueForm(request.POST , request.FILES)
        if form.is_valid():
            venue = form.save(commit=False)
            venue.owner = request.user.id
            form.save()
            return HttpResponseRedirect('/venues?submitted')
    else :
        form = VenueForm()
        if 'submitted' in request.GET :
            submitted= True

    return render(request , 'event/Venue_form.html' , {'form':form , 'submitted': submitted})

def event_l(request):
    #event_list = Event.objects.all().order_by('name')

    p = Paginator(Event.objects.all() , 8)
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

    event_list = Event.objects.filter(date__year = datetime.now().year , date__month = datetime.now().month)

    context = {
        'name': name,
        'month_number': month_number,
        'cal': cal,
        'year': year,
        'month': month,
        'event_list':event_list
    }
    return render(request, 'event/home.html', context)

