from rest_framework import generics

from core.models.image import Image
from core.serializers.image_serializer import ImageSerializer


class ImageCreateView(generics.CreateAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer