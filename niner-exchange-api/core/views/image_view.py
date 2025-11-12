from rest_framework import generics, permissions, status
from rest_framework.response import Response

from core.models.image import Image
from core.serializers.image_serializer import ImageSerializer


class ImageCreateView(generics.CreateAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        
        data = serializer.validated_data
        listing = data['listing']
        upload_orders = request.data.getlist('upload_order')
        images = request.data.getlist('image')

        new_images = []
        for i in range(len(upload_orders)):
            new_image = Image.objects.create(listing=listing, image=images[i], upload_order=upload_orders[i])
            new_images.append(new_image)

        created_serializer = self.get_serializer(new_images, many=True)
        return Response(created_serializer.data, status=status.HTTP_201_CREATED)
