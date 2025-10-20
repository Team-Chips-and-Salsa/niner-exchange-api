from rest_framework import serializers

from core.models.image import Image
from core.models.listing import Listing


class ImageSerializer(serializers.ModelSerializer):
    listing = serializers.PrimaryKeyRelatedField(queryset=Listing.objects.all())
    #image = serializers.URLField(source='image.url', read_only=True)

    class Meta:
        model = Image
        fields = [
            'image_id',
            'listing',
            'upload_order',
            'image',
        ]
        read_only_fields = ['image_id']

    # Use AI to fix the image URL representation
    def to_representation(self, instance):
        # Get the default representation (includes the path/public ID for 'image')
        representation = super().to_representation(instance)

        # Explicitly replace the 'image' value with the full URL
        if instance.image and hasattr(instance.image, 'url'):
            representation['image'] = instance.image.url

        return representation

    def validate_listing(self, listing):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError("Authentication required.")

        # Ensure the listing belongs to the authenticated user
        if listing.seller != request.user:
            raise serializers.ValidationError("You can only add images to your own listings.")

        return listing

    def validate(self, attrs):
        listing = attrs.get('listing')

        # Check if we are updating or creating
        is_create = self.instance is None

        if listing and is_create and listing.images.count() >= 3:
            # Max 3 images per listing
            raise serializers.ValidationError("You cannot upload more than 3 images per listing.")

        return attrs