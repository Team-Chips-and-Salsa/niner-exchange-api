from rest_framework import serializers
from core.models.report import Report
from core.models.listing import Listing
from core.models.user import CustomUser
from core.models.review import Review
from core.serializers.review_serializer import PopulatedReviewSerializer
from core.serializers.listing_serializer import ListingSellerSerializer, ListingSerializer

class ReportSerializer(serializers.ModelSerializer):
    reporter = ListingSellerSerializer(read_only=True)
    content_object = serializers.SerializerMethodField()

    # Used to distinguish between teh different types of reports
    def get_content_object(self, obj):
        target_object = obj.content_object

        if isinstance(target_object, Listing):
            return ListingSerializer(target_object, context=self.context).data
        elif isinstance(target_object, CustomUser):
            return ListingSellerSerializer(target_object, context=self.context).data
        elif isinstance(target_object, Review):
            return PopulatedReviewSerializer(target_object, context=self.context).data

    class Meta:
        model = Report
        fields = [
            "id",
            'content_type',
            'object_id',
            'content_object',
            'reporter',
            'reason',
            'status',
            'description',
            'created_at',
        ]

        read_only_fields = ["id", "reporter", "created_at", "content_object"]

    def create(self, validated_data):
        validated_data['reporter'] = self.context['request'].user
        return super().create(validated_data)
    
    
class ReportStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Report
        fields = ["status"]

    def validate_status(self, value):
        instance = self.instance

        valid_statuses = [choice[0] for choice in Report.STATUS_CHOICES]
        if value not in valid_statuses:
            raise serializers.ValidationError(f"'{value}' is not a valid status.")

        current_status = instance.status

        if current_status == "APPROVED":
            raise serializers.ValidationError(
                "A 'APPROVED' report's status cannot be changed."
            )

        if current_status == "DENIED":
            raise serializers.ValidationError(
                "A 'DENIED' report's status cannot be changed."
            )

        return value