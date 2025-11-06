import django_filters
from rest_framework import generics, permissions

from core.models.listing import Service
from core.serializers.listing_serializer import ServiceSerializer


class ServiceListCreateView(generics.ListCreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filterset_fields = ["status"]
