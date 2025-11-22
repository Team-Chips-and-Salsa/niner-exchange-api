from rest_framework import serializers

from core.models.image import Image
from core.models.listing import Listing


class ImageSerializer(serializers.ModelSerializer):
    listing = serializers.PrimaryKeyRelatedField(queryset=Listing.objects.all())

    class Meta:
        model = Image
        fields = [
            "image_id",
            "listing",
            "upload_order",
            "image",
        ]
        read_only_fields = ["image_id"]
        validators =[]

    # Used AI to fix representation of image URL
    def to_representation(self, instance):
        representation = super().to_representation(instance)

        if instance.image and hasattr(instance.image, "url"):
            representation["image"] = instance.image.url
        else:
            representation["image"] = None

        return representation

    def validate_listing(self, listing):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError("Authentication required.")

        if listing.seller != request.user:
            raise serializers.ValidationError(
                "You can only add images to your own listings."
            )

        return listing

    def validate(self, attrs):
        listing = attrs.get("listing")

        # Check if we are updating or creating
        is_create = self.instance is None

        if listing and is_create and listing.images.count() >= 3:
            raise serializers.ValidationError(
                "You cannot upload more than 3 images per listing."
            )

        return attrs
