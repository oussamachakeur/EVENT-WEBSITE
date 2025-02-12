
from django.contrib import admin
from django.urls import path , include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('' , include('event.urls')),
]



admin.site.site_header="my club admin"
admin.site.site_title = "my club admin"
admin.site.index_title= "hello to the admin area"