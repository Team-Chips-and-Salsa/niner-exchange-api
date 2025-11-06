from django.urls import path

from core.views.sublease_view import SubleaseListCreateView

urlpatterns = [
    path("subleases/", SubleaseListCreateView.as_view(), name="sublease-list-create"),
]
