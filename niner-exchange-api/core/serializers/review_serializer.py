from rest_framework import serializers
from core.models.review import Review
from core.models.transaction import Transaction
from core.models.user import CustomUser
from core.serializers.listing_serializer import ListingMinimalSerializer
from core.serializers.user_serializer import (
    ListingSellerSerializer,
)


class ReviewCreateSerializer(serializers.ModelSerializer):
    transaction = serializers.PrimaryKeyRelatedField(queryset=Transaction.objects.all())
    reviewee = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())

    class Meta:
        model = Review
        fields = [
            "review_id",
            "transaction",
            "reviewee",
            "rating",
            "comment",
            "created_at",
            "reviewer",
        ]
        read_only_fields = ["review_id", "created_at", "reviewer"]

    def validate(self, attrs):
        request = self.context.get("request")
        reviewer = request.user
        reviewee = attrs.get("reviewee")
        transaction = attrs.get("transaction")

        if reviewer == reviewee:
            raise serializers.ValidationError("You cannot review yourself.")

        if reviewer != transaction.buyer and reviewer != transaction.seller:
            raise serializers.ValidationError(
                "You were not a participant in this transaction."
            )

        if (reviewer == transaction.buyer and reviewee != transaction.seller) or (
            reviewer == transaction.seller and reviewee != transaction.buyer
        ):
            raise serializers.ValidationError(
                "You can only review the other participant of the transaction."
            )

        if transaction.status != "COMPLETED":
            raise serializers.ValidationError(
                "You can only review a completed transaction."
            )

        if Review.objects.filter(transaction=transaction, reviewer=reviewer).exists():
            raise serializers.ValidationError(
                "You have already reviewed this transaction."
            )

        return attrs

    def create(self, validated_data):
        validated_data["reviewer"] = self.context["request"].user
        return super().create(validated_data)


class PopulatedReviewSerializer(serializers.ModelSerializer):
    reviewer = ListingSellerSerializer(read_only=True)
    listing = ListingMinimalSerializer(source="transaction.listing", read_only=True)

    class Meta:
        model = Review
        fields = [
            "review_id",
            "reviewer",
            "listing",
            "rating",
            "comment",
            "created_at",
        ]
