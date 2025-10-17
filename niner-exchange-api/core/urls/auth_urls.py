from django.urls import path

from core.views.user_view import LoginView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
]