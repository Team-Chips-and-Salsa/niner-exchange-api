from django.urls import path

from core.views.user_view import GetUserView, GetMeView
from core.views.purchase_history_view import PurchaseHistoryView

urlpatterns = [
    path("users/<uuid:id>/", GetUserView.as_view(), name="user-detail"),
    path('users/purchase-history/<uuid:id>/', PurchaseHistoryView.as_view(), name="user-purchase-history"),
]