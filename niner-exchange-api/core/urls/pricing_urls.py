from django.urls import path
from core.views.pricing_view import suggest_price

urlpatterns = [
    path('suggest/', suggest_price, name='suggest_price'),
]

