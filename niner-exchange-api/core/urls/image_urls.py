from django.urls import path

from core.views.image_view import ImageCreateView

urlpatterns = [
    path('images/', ImageCreateView.as_view(), name="image-create"),
]