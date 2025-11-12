import decimal
from rest_framework import serializers
from core.models.listing import Listing, ItemListing, TextbookListing, Sublease, Service, PhysicalListing
from core.serializers.image_serializer import ImageSerializer


class ListingSerializer(serializers.ModelSerializer):

    seller = serializers.SlugRelatedField(read_only=True, slug_field="email")
    images = serializers.SerializerMethodField()
    listing_type = serializers.SerializerMethodField()

    class Meta:
        model = Listing
        fields = [
            "listing_id",
            "seller",
            "title",
            "description",
            "price",
            "status",
            "created_at",
            "updated_at",
            "images",
            "listing_type",
        ]
        read_only_fields = [
            "listing_id",
            "status",
            "created_at",
            "updated_at",
            "listing_type",
        ]

    def get_images(self, obj):
        qs = obj.images.order_by("upload_order")
        return ImageSerializer(qs, many=True, context=self.context).data

    def get_listing_type(self, obj):
        if hasattr(obj, "sublease"):
            return "sublease"
        elif hasattr(obj, "service"):
            return "service"
        elif hasattr(obj, "textbooklisting"):
            return "textbook"
        elif hasattr(obj, "itemlisting"):
            return "item"
        elif hasattr(obj, "physicallisting"):
            return "physical"
        else:
            return "listing"

    def validate_price(self, value):
        if value <= decimal.Decimal("0.00"):
            raise serializers.ValidationError("Price must be a positive number.")

        if value < decimal.Decimal("1"):
            raise serializers.ValidationError("Price must be at least $1.")

        return value

    def validate(self, attrs):
        title = attrs.get("title")
        description = attrs.get("description")

        if title and description and title.lower() == description.lower():
            raise serializers.ValidationError(
                "Title and description cannot be the same."
            )

        return attrs

    def create(self, validated_data):
        validated_data["seller"] = self.context["request"].user

        validated_data["status"] = "ACTIVE"

        return super().create(validated_data)


class ListingStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Listing
        fields = ["status"]

    def validate_status(self, value):
        instance = self.instance

        valid_statuses = [choice[0] for choice in Listing.STATUS_CHOICES]
        if value not in valid_statuses:
            raise serializers.ValidationError(f"'{value}' is not a valid status.")

        current_status = instance.status

        if current_status == "SOLD":
            raise serializers.ValidationError(
                "A 'SOLD' item's status cannot be changed."
            )

        if current_status == "REMOVE" and value not in ["ACTIVE"]:
            raise serializers.ValidationError(
                "A removed item can only be re-activated."
            )

        return value

class PhysicalListingSerializer(ListingSerializer):
    class Meta(ListingSerializer.Meta):
        model = PhysicalListing
        fields = ListingSerializer.Meta.fields + ["condition", "price_new"]

class ItemListingSerializer(ListingSerializer):
    class Meta(ListingSerializer.Meta):
        model = ItemListing
        fields = ListingSerializer.Meta.fields + ["condition", "price_new"]


class TextbookListingSerializer(ListingSerializer):
    class Meta(ListingSerializer.Meta):
        model = TextbookListing
        fields = ListingSerializer.Meta.fields + ["condition", "course_code", "price_new"]


class SubleaseSerializer(ListingSerializer):
    class Meta(ListingSerializer.Meta):
        model = Sublease
        fields = ListingSerializer.Meta.fields + [
            "property_type",
            "start_date",
            "end_date",
            "number_of_bedrooms",
            "number_of_roommates",
            "distance_from_campus_minutes",
        ]

    def validate(self, attrs):
        # Call parent validation
        attrs = super().validate(attrs)

        # Additional validation for Sublease
        start_date = attrs.get("start_date")
        end_date = attrs.get("end_date")

        if start_date and end_date and start_date >= end_date:
            raise serializers.ValidationError("End date must be after start date.")

        return attrs


class ServiceSerializer(ListingSerializer):

    class Meta(ListingSerializer.Meta):
        model = Service
        fields = ListingSerializer.Meta.fields
