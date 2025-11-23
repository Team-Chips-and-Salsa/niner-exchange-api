from django.contrib import admin
from django.urls import path, include  

from core.views.auth_views.health_view import HealthCheckView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("health/", HealthCheckView.as_view(), name="health-check"),
    path(
        "api/auth/", include("core.urls.auth_urls")
    ),  # Authentication endpoints (login, register)
    path(
        "api/", include("core.urls.transaction_urls")
    ),  # Public Transaction API endpoints
    path("api/", include("core.urls.listing_urls")),  # Public Listing API endpoints
    path("api/", include("core.urls.item_listing_urls")),  # Item Listing API endpoints
    path(
        "api/", include("core.urls.textbook_listing_urls")
    ),  # Textbook Listing API endpoints
    path("api/", include("core.urls.sublease_urls")),  # Sublease API endpoints
    path("api/", include("core.urls.service_urls")),  # Service API endpoints
    path("api/", include("core.urls.image_urls")),  # Public Image API endpoints
    path(
        "api/pricing/", include("core.urls.pricing_urls")
    ),  # Pricing-related API endpoints
    path("api/", include("core.urls.user_urls")),  # User-related API endpoints
    path("api/", include("core.urls.review_urls")),  # Review-related API endpoints
    path("api/admin/", include("core.urls.admin_urls")),
    path("api/", include("core.urls.report_urls")),
    path("api/", include("core.urls.meetup_location_urls"))
]
