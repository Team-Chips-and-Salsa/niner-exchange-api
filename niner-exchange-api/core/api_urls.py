from django.urls import path
from .views import (
    MeetupLocationListView,
    TransactionCreateView,
    TransactionStatusUpdateView,
    ListingCreateView,
    ListingListView,
    ListingUpdateView,
    CategoryCreateView,
    ImageCreateView,
)

urlpatterns = [
    path('meetup-locations/', MeetupLocationListView.as_view(), name='meetup-location-list'),
    path('transactions/', TransactionCreateView.as_view(), name='transaction-create'),
    path('transactions/<uuid:id>/', TransactionStatusUpdateView.as_view(), name='transaction-status-update'),
    path('listings/', ListingCreateView.as_view(), name="listing-create"),
    path('listings/', ListingListView.as_view(), name="listing-view-all"),
    path('listings/<uuid:listing_id>/', ListingUpdateView.as_view(), name="listing-update"),
    path('categories/', CategoryCreateView.as_view(), name="category-create"),
    path('images/', ImageCreateView.as_view(), name="image-create"),
]

