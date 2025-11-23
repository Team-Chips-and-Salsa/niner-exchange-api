from django.urls import path

from core.views.admin_view import FlaggedReportView, ContentTypeView, FlaggedReportStatusUpdateView, MeetupLocationCreateView, MeetupLocationDetailView, UserListView

urlpatterns = [
    path('reports/', FlaggedReportView.as_view(), name='report-view'),
    
    path('meetup-locations/<int:pk>/', MeetupLocationDetailView.as_view(), name='admin-meetup-location-detail-view'),
    path('meetup-locations/create/', MeetupLocationCreateView.as_view(), name='admin-meetup-location-create-view'),
    path('content-types/', ContentTypeView.as_view(), name='content-types-view'),
    path('reports/<int:id>/status/', FlaggedReportStatusUpdateView.as_view(), name="report-status-update"),
    path('users/', UserListView.as_view(), name='user-list-view'),
]