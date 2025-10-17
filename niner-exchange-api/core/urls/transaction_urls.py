from django.urls import path

from core.views.transaction_view import TransactionCreateView, TransactionStatusUpdateView

urlpatterns = [
    path('transactions/', TransactionCreateView.as_view(), name='transaction-create'),
    path('transactions/<uuid:id>/', TransactionStatusUpdateView.as_view(), name='transaction-status-update'),
]