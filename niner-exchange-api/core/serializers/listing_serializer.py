import decimal
from rest_framework import serializers
from core.models.listing import Listing
from core.serializers.image_serializer import ImageSerializer


class ListingSerializer(serializers.ModelSerializer):

    seller = serializers.SlugRelatedField(read_only=True, slug_field='email')
    images = serializers.SerializerMethodField()
    class Meta:
        model = Listing
        fields = [
            'listing_id',
            'seller',
            'category',
            'title',
            'description',
            'price',
            'condition',
            'status',
            'created_at',
            'updated_at',
            'images',
        ]
        read_only_fields = ['listing_id', 'status', 'created_at', 'updated_at']

    def get_images(self, obj):
            qs = obj.images.order_by('upload_order')
            return ImageSerializer(qs, many=True, context=self.context).data

    def validate_price(self, value):
        if value <= decimal.Decimal('0.00'):
            raise serializers.ValidationError("Price must be a positive number.")

        if value < decimal.Decimal('1'):
            raise serializers.ValidationError("Price must be at least $1.")

        return value

    def validate(self, attrs):
        title = attrs.get('title')
        description = attrs.get('description')

        if title and description and title.lower() == description.lower():
            raise serializers.ValidationError("Title and description cannot be the same.")

        return attrs

    def create(self, validated_data):
        validated_data['seller'] = self.context['request'].user

        validated_data['status'] = 'ACTIVE'

        return super().create(validated_data)


class ListingStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Listing
        fields = ['status']

    def validate_status(self, value):
        instance = self.instance

        valid_statuses = [choice[0] for choice in Listing.STATUS_CHOICES]
        if value not in valid_statuses:
            raise serializers.ValidationError(f"'{value}' is not a valid status.")

        current_status = instance.status

        if current_status == 'SOLD':
            raise serializers.ValidationError("A 'SOLD' item's status cannot be changed.")

        if current_status == 'REMOVE' and value not in ['ACTIVE']:
            raise serializers.ValidationError("A removed item can only be re-activated.")

        return value