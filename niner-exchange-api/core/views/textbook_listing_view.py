import django_filters
from rest_framework import generics, permissions

from core.models.listing import TextbookListing
from core.serializers.listing_serializer import TextbookListingSerializer
from core.throttles import ListingCreationThrottle

class TextbookListingListCreateView(generics.ListCreateAPIView):
    queryset = TextbookListing.objects.all()
    serializer_class = TextbookListingSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [ListingCreationThrottle]

    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filterset_fields = ["status", "condition", "course_code"]
