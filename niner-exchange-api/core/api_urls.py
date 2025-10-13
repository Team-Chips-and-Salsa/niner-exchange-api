from django.urls import path
from .views import (
    MeetupLocationListView,
    TransactionCreateView,
    TransactionStatusUpdateView,
)

urlpatterns = [
    path('meetup-locations/', MeetupLocationListView.as_view(), name='meetup-location-list'),
    path('transactions/', TransactionCreateView.as_view(), name='transaction-create'),
    path('transactions/<uuid:id>/', TransactionStatusUpdateView.as_view(), name='transaction-status-update'),
]

