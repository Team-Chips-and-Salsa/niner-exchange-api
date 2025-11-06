from django.urls import path

from core.views.item_listing_view import ItemListingListCreateView

urlpatterns = [
    path(
        "items/", ItemListingListCreateView.as_view(), name="item-listing-list-create"
    ),
]
