from rest_framework import serializers
from core.models.meetup_location import MeetupLocation

class MeetupLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetupLocation
        fields = ['id', 'name', 'description', 'latitude', 'longitude']