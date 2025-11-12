import django_filters
from rest_framework import generics, permissions
from rest_framework.response import Response
from django.db.models import Prefetch

from core.filters.listing_filter import ListingFilter
from core.models.listing import Listing, ItemListing, TextbookListing, Sublease, Service, PhysicalListing
from core.serializers.listing_serializer import (
    ListingSerializer,
    ListingStatusSerializer,
    ItemListingSerializer,
    TextbookListingSerializer,
    SubleaseSerializer,
    ServiceSerializer,
    PhysicalListingSerializer,
)


class ListingListCreateView(generics.ListCreateAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filterset_class = ListingFilter

    def get_queryset(self):
        queryset = Listing.objects.select_related("seller").prefetch_related("images")

        return queryset

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ListingSerializer
        return ListingSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serialized_data = [
                self._get_serialized_listing(listing) for listing in page
            ]
            return self.get_paginated_response(serialized_data)

        serialized_data = [
            self._get_serialized_listing(listing) for listing in queryset
        ]
        return Response(serialized_data)

    def _get_serialized_listing(self, listing):
        # Check if listing is a Sublease
        if hasattr(listing, "sublease"):
            serializer = SubleaseSerializer(
                listing.sublease, context={"request": self.request}
            )
        # Check if listing is a Service
        elif hasattr(listing, "service"):
            serializer = ServiceSerializer(
                listing.service, context={"request": self.request}
            )
        # Check if listing is a TextbookListing
        elif hasattr(listing, "textbooklisting"):
            serializer = TextbookListingSerializer(
                listing.textbooklisting, context={"request": self.request}
            )
        # Check if listing is an ItemListing
        elif hasattr(listing, "itemlisting"):
            serializer = ItemListingSerializer(
                listing.itemlisting, context={"request": self.request}
            )
        # Check if listing is a PhysicalListing (but not Item or Textbook)
        elif hasattr(listing, "physicallisting"):
            # This shouldn't happen if we don't create PhysicalListing directly
            serializer = ListingSerializer(listing, context={"request": self.request})
        else:
            # Base Listing
            serializer = ListingSerializer(listing, context={"request": self.request})

        return serializer.data


class ListingUpdateView(generics.UpdateAPIView):
    serializer_class = ListingSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "listing_id"

    def get_queryset(self):
        return Listing.objects.filter(seller=self.request.user)


class ListingStatusUpdateView(generics.UpdateAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingStatusSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "listing_id"

    def get_queryset(self):
        return Listing.objects.filter(seller=self.request.user)

    def patch(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)


class GetListingView(generics.RetrieveAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "listing_id"

    def get_object(self):
        # Get the base listing object
        listing = super().get_object()

        # Return the specific subclass instance
        if hasattr(listing, "sublease"):
            return listing.sublease
        elif hasattr(listing, "service"):
            return listing.service
        elif hasattr(listing, "physicallisting"):
            if hasattr(listing.physicallisting, "textbooklisting"):
                return listing.physicallisting.textbooklisting
            if hasattr(listing.physicallisting, "itemlisting"):
                return listing.physicallisting.itemlisting
            return listing.physicallisting
        else:
            return listing

    def get_serializer_class(self):
        listing = self.get_object()

        if isinstance(listing, Sublease):
            return SubleaseSerializer
        elif isinstance(listing, Service):
            return ServiceSerializer
        elif isinstance(listing, TextbookListing):
            return TextbookListingSerializer
        elif isinstance(listing, ItemListing):
            return ItemListingSerializer
        elif isinstance(listing, PhysicalListing):
            return PhysicalListingSerializer
        else:
            return ListingSerializer
