from rest_framework import permissions, generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
import cloudinary.uploader

from core.models.user import CustomUser
from core.serializers.user_serializer import UserSerializer


class GetUserView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "id"


class GetMeView(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
    
class UpdateMeView(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

class UserImageUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        image = request.FILES.get('image')

        if not image:
            return Response({'error': 'No image provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Upload to Cloudinary
            upload_result = cloudinary.uploader.upload(image)
            image_url = upload_result.get('secure_url')

            # Update user profile
            user.profile_image_url = image_url
            user.save()

            return Response({'profile_image_url': image_url}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
