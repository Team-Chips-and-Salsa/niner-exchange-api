from rest_framework import generics, permissions

from core.models.meetup_location import MeetupLocation
from core.serializers.meetup_location_serializer import MeetupLocationSerializer


class MeetupLocationListView(generics.ListCreateAPIView):
    queryset = MeetupLocation.objects.all().order_by('name')
    serializer_class = MeetupLocationSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]