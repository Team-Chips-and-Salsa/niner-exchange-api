from django.urls import path

from core.views.user_view import GetUserView, GetMeView, UpdateMeView
from core.views.purchase_history_view import PurchaseHistoryView
from core.views.listing_view import UserActiveListingListView, UserSoldListingListView

urlpatterns = [
    path("users/<uuid:id>/", GetUserView.as_view(), name="user-detail"),
    path('users/me/update/', UpdateMeView.as_view(), name='update-me'),
    path('users/current-listings/<uuid:id>/', UserActiveListingListView.as_view(), name='user-active-listings'),
    path('users/sold-listings/<uuid:id>/', UserSoldListingListView.as_view(), name='user-sold-listings'),
    path('users/purchase-history/<uuid:id>/', PurchaseHistoryView.as_view(), name='user-purchase-history'),

]