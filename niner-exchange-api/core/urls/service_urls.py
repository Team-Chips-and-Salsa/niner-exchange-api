from django.urls import path

from core.views.service_view import ServiceListCreateView

urlpatterns = [
    path("services/", ServiceListCreateView.as_view(), name="service-list-create"),
]
