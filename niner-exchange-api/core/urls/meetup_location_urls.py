from django.urls import path

from core.views.admin_view import MeetupLocationListView

urlpatterns = [
    path('meetup-locations/', MeetupLocationListView.as_view(), name='admin-meetup-location-list'),
]