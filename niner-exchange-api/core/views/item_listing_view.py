import django_filters
from rest_framework import generics, permissions

from core.models.listing import ItemListing
from core.serializers.listing_serializer import ItemListingSerializer


class ItemListingListCreateView(generics.ListCreateAPIView):
    queryset = ItemListing.objects.all()
    serializer_class = ItemListingSerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filterset_fields = ["status", "condition"]
