from django.urls import path

from core.views.textbook_listing_view import TextbookListingListCreateView

urlpatterns = [
    path(
        "textbooks/",
        TextbookListingListCreateView.as_view(),
        name="textbook-listing-list-create",
    ),
]
