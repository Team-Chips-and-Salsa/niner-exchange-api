from django.urls import path

from core.views.admin_view import ReportCreateView

urlpatterns = [
    path('reports/create/', ReportCreateView.as_view(), name='report-create-view'),
]