from django.contrib import admin
from django.urls import path, include # Add 'include' here

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('core.urls.auth_urls')),  # Authentication endpoints (login, register)
    path('api/', include('core.urls.meetup_location_urls')),  # Public Meetup Locations API endpoints
    path('api/', include('core.urls.transaction_urls')),  # Public Transaction API endpoints

]
