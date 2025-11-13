from rest_framework import serializers

from core.models.user import CustomUser


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the CustomUser model.

    Intended for returning safe user data to the frontend. Fields are read-only by
    default; update endpoints should use a dedicated serializer that validates
    editable fields.
    """

    id = serializers.CharField(read_only=True)
    avg_rating = serializers.DecimalField(max_digits=3, decimal_places=2, read_only=True)
    review_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = CustomUser
        # Expose fields useful for a profile page and for the authenticated user
        fields = [
            'id',
            'first_name',
            'last_name',
            'date_joined',
            'email',
            'profile_image_url',
            'avg_rating',
            'review_count',
            'status',
            'role',
            'updated_at',
        ]
        read_only_fields = ['id', 'avg_rating', 'review_count', 'updated_at']

    def to_representation(self, instance):
        """Customize representation if needed (e.g. format avg_rating as float)."""
        data = super().to_representation(instance)
        # Ensure avg_rating is returned as a numeric value (not Decimal) when present
        avg = data.get('avg_rating')
        if avg is not None:
            try:
                data['avg_rating'] = float(avg)
            except (TypeError, ValueError):
                pass
        return data
