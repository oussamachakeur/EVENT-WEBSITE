from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('event.urls'), name='home'),  
    path('members/', include('django.contrib.auth.urls')),  
    path('members/', include('members.urls')),  
]+static(settings.MEDIA_URL , document_root= settings.MEDIA_ROOT , )

admin.site.site_header="my club admin"
admin.site.site_title = "my club admin"
admin.site.index_title= "hello to the admin area"

