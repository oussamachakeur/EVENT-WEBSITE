from django.contrib import admin
from .models import Venue , MyUser , Event
# Register your models here.


#admin.site.register(Venue)
admin.site.register(MyUser)
#admin.site.register(Event)


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display=('name' , 'address' , 'phone')
    ordering = ('-name',)
    search_fields=('name','address')



@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    fields=(('name','date'),('venue','manager'),'description')
    list_display=('name','date','manager')
    list_filter=('name', 'date')
    ordering=('name',)
