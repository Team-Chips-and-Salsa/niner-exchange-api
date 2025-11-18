from django.urls import path

from core.views.review_view import ReviewCreateView, UserReviewListView

urlpatterns = [
    path("reviews/", ReviewCreateView.as_view(), name="review-create"),
    path(
        "users/<uuid:user_id>/reviews/",
        UserReviewListView.as_view(),
        name="user-review-list",
    ),
]
