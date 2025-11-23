from rest_framework import serializers

from core.models.meetup_location import MeetupLocation

class MeetupLocationSerializer(serializers.ModelSerializer):
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()

    class Meta:
        model = MeetupLocation
        fields = ['id', 'name', 'description', 'latitude', 'longitude', 'is_active']