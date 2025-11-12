from django.contrib import admin
from django.urls import path, include # Add 'include' here

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('core.urls.auth_urls')),  # Authentication endpoints (login, register)
    path('api/', include('core.urls.meetup_location_urls')),  # Public Meetup Locations API endpoints
    path('api/', include('core.urls.transaction_urls')),  # Public Transaction API endpoints
    path('api/', include('core.urls.listing_urls')), # Public Listing API endpoints
    path('api/', include('core.urls.image_urls')), # Public Image API endpoints
    path('api/', include('core.urls.category_urls')), # Public Category API endpoints
    path('api/', include('core.urls.user_urls')),  # User-related API endpoints
    path('api/pricing/', include('core.urls.pricing_urls')), # Pricing-related API endpoints
]
