from django.urls import path

from core.views.listing_view import ListingListCreateView, ListingStatusUpdateView, ListingUpdateView, GetListingView, ListingDeleteView
from core.views.purchase_history_view import PurchaseHistoryView

urlpatterns = [
    path('listings/', ListingListCreateView.as_view(), name="listing-list-create"),
    path('listings/<uuid:listing_id>/', GetListingView.as_view(), name='listing-detail'),
    path('listings/<uuid:listing_id>/edit/', ListingUpdateView.as_view(), name="listing-detail-update"),
    path('listings/<uuid:listing_id>/delete/', ListingDeleteView.as_view(), name="listing-detail-delete"),
    path('listings/<uuid:listing_id>/status/', ListingStatusUpdateView.as_view(), name="listing-status-update"),
]