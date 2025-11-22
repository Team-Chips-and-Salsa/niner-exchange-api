from django.urls import path

from core.views.transaction_view import (
    TransactionCreateView,
    TransactionStatusUpdateView,
    TransactionRetrieveView,
)

urlpatterns = [
    path("transactions/", TransactionCreateView.as_view(), name="transaction-create"),
    path(
        "transactions/<uuid:id>/",
        TransactionRetrieveView.as_view(),
        name="transaction-detail",
    ),
    path(
        "transactions/<uuid:id>/update-status/",
        TransactionStatusUpdateView.as_view(),
        name="transaction-status-update",
    ),
]
