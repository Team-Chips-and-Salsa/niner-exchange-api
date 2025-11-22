from django.urls import path

from core.views.admin_view import FlaggedReportView, ExchangeZonesView, ContentTypeView, FlaggedReportStatusUpdateView

urlpatterns = [
    path('reports/', FlaggedReportView.as_view(), name='report-view'),
    path('exchange-zones/', ExchangeZonesView.as_view(), name='admin-exchange-zones-view'),
    path('content-types/', ContentTypeView.as_view(), name='content-types-view'),
    path('reports/<int:id>/status/', FlaggedReportStatusUpdateView.as_view(), name="report-status-update"),
]