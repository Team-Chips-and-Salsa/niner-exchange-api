from django.db.models import Q
from rest_framework import generics, permissions

from core.models.transaction import Transaction
from core.serializers.transaction_serializer import TransactionSerializer, TransactionStatusSerializer


class TransactionCreateView(generics.CreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

class TransactionStatusUpdateView(generics.UpdateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionStatusSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    # Improve security with AI
    def get_queryset(self):
        user = self.request.user
        return Transaction.objects.filter(Q(buyer=user) | Q(seller=user))

    def patch(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
