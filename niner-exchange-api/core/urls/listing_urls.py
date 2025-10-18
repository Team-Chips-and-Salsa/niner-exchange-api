from django.urls import path

from core.views.listing_view import ListingListCreateView, ListingStatusUpdateView, ListingUpdateView

urlpatterns = [
    path('listings/', ListingListCreateView.as_view(), name="listing-list-create"),
    path('listings/<uuid:listing_id>/', ListingUpdateView.as_view(), name="listing-detail-update"),
    path('listings/<uuid:listing_id>/status/', ListingStatusUpdateView.as_view(), name="listing-status-update"),
]