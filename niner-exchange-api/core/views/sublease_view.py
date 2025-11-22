import django_filters
from rest_framework import generics, permissions

from core.models.listing import Sublease
from core.serializers.listing_serializer import SubleaseSerializer
from core.throttles import ListingCreationThrottle


class SubleaseListCreateView(generics.ListCreateAPIView):
    queryset = Sublease.objects.all()
    serializer_class = SubleaseSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [ListingCreationThrottle]

    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filterset_fields = ["status", "property_type", "number_of_bedrooms", "physical_address"]
