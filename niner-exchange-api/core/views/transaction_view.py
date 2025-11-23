from django.db.models import Q
from rest_framework import generics, permissions
from firebase_admin import firestore

from core.models.transaction import Transaction
from core.serializers.transaction_serializer import (
    TransactionSerializer,
    TransactionStatusSerializer,
    PopulatedTransactionSerializer,
)


class TransactionCreateView(generics.CreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]


class TransactionStatusUpdateView(generics.UpdateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionStatusSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "id"

    # Improved security with AI
    def get_queryset(self):
        user = self.request.user
        return Transaction.objects.filter(Q(buyer=user) | Q(seller=user))

    def patch(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)

    def perform_update(self, serializer):
        instance = serializer.save()

        if instance.status == "COMPLETED":

            listing = instance.listing
            if listing.status != "SOLD":
                listing.status = "SOLD"
                listing.save()

            Transaction.objects.filter(listing=listing, status="PENDING").exclude(
                id=instance.id
            ).update(status="REJECTED")

            try:
                db = firestore.client()

                notification_data = {
                    "userId": str(instance.buyer.id),
                    "message": f"Your transaction for '{listing.title}' was completed. Review the seller.",
                    "is_read": False,
                    "created_at": firestore.SERVER_TIMESTAMP,
                    "link_to": f"/review-user/{instance.seller.id}/{instance.id}",
                    "transactionId": str(instance.id),
                }

                db.collection("notifications").add(notification_data)

            except Exception as e:
                print(f"Failed to create notification: {str(e)}")


class TransactionRetrieveView(generics.RetrieveAPIView):
    serializer_class = PopulatedTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "id"

    def get_queryset(self):
        return Transaction.objects.filter(
            Q(buyer=self.request.user) | Q(seller=self.request.user)
        ).select_related("listing", "buyer", "seller")
