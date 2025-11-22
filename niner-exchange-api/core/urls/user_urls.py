from django.urls import path

from core.views.review_view import ReviewCreateView, UserReviewListView
from core.views.user_view import GetUserView, GetMeView

urlpatterns = [
    path("users/<uuid:id>/", GetUserView.as_view(), name="user-detail"),
]
