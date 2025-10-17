from django.urls import path

from core.views.meetup_location_view import MeetupLocationListView

urlpatterns = [
    path('meetup-locations/', MeetupLocationListView.as_view(), name='meetup-location-list'),
]