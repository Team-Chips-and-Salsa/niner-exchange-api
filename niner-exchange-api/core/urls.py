from django.urls import path
from .views import LoginView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    # Add urls for listings
]