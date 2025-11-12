from django.urls import path

from core.views.user_view import GetUserView


urlpatterns = [
    path('users/<uuid:id>/', GetUserView.as_view(), name='user-detail'),
]