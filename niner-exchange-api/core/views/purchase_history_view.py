from rest_framework import generics, permissions
from core.models.transaction import Transaction

from core.serializers.listing_serializer import PurchaseHistorySerializer

class PurchaseHistoryView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated] 
    serializer_class = PurchaseHistorySerializer

    def get_queryset(self):
        buyer_id = self.kwargs.get('id')
        
        return Transaction.objects.filter(
            buyer__id=buyer_id, 
            status='PENDING'
        ).select_related('listing', 'listing__seller').prefetch_related('listing__images').order_by('-updated_at')