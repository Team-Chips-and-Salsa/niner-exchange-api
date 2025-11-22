from django.db.models import Count
from rest_framework import serializers
from django.core.exceptions import ValidationError
from core.models.user import CustomUser


class UserSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    avg_rating = serializers.DecimalField(
        max_digits=3, decimal_places=2, read_only=True
    )
    review_count = serializers.IntegerField(read_only=True)
    rating_breakdown = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "first_name",
            "last_name",
            "date_joined",
            "email",
            "profile_image_url",
            "avg_rating",
            "review_count",
            "rating_breakdown",
            "status",
            "role",
            "updated_at",
            "items_sold_count",
            "bio",
            "is_verified_student",
            "last_active",
        ]
        read_only_fields = [
            "id",
            "avg_rating",   
            "review_count",
            "updated_at",
            "date_joined",       
            "email",           
            "is_verified_student",
            "items_sold_count",   
            "last_active",        
        ]   


    def to_representation(self, instance):
        data = super().to_representation(instance)
        avg = data.get("avg_rating")
        if avg is not None:
            try:
                data["avg_rating"] = float(avg)
            except (TypeError, ValueError):
                pass
        return data

    def get_rating_breakdown(self, obj):
        breakdown = {5: 0, 4: 0, 3: 0, 2: 0, 1: 0}

        counts = obj.reviews_received.values("rating").annotate(count=Count("rating"))

        for item in counts:
            if item["rating"] in breakdown:
                breakdown[item["rating"]] = item["count"]

        return breakdown


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("email", "password", "first_name", "last_name")
        extra_kwargs = {
            "password": {
                "write_only": True,
                "style": {"input_type": "password"},
                "required": True,
            },
            "first_name": {"required": True},
            "last_name": {"required": True},
        }

    # Used AI to validate Email and figure out how to send an email
    def validate_email(self, value):
        if not value.endswith("@charlotte.edu"):
            raise serializers.ValidationError(
                "Only @charlotte.edu email addresses are allowed."
            )

        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email address is already in use.")

        return value

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            is_active=False,
        )
        return user


class ListingSellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "first_name",
            "last_name",
            "avg_rating",
            "review_count",
            "profile_image_url",
            "date_joined",
        ]
        read_only_fields = fields
