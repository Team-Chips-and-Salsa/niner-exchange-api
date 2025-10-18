from rest_framework import generics, permissions

from core.models.listing import Listing
from core.serializers.listing_serializer import ListingSerializer, ListingStatusSerializer


class ListingListCreateView(generics.ListCreateAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [permissions.IsAuthenticated]

class ListingUpdateView(generics.UpdateAPIView):
    serializer_class = ListingSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'listing_id'

    def get_queryset(self):
        return Listing.objects.filter(seller=self.request.user)

class ListingStatusUpdateView(generics.UpdateAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingStatusSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'listing_id'

    def get_queryset(self):
        return Listing.objects.filter(seller=self.request.user)

    def patch(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)