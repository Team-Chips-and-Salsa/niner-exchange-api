from django.contrib.auth import authenticate

from rest_framework.generics import RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, generics
from rest_framework_simplejwt.tokens import RefreshToken

from firebase_admin import auth as firebase_auth

from core.models.user import CustomUser
from core.serializers.user_serializer import UserSerializer

class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'error': 'Email and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Authenticate the user with Django's system
        user = authenticate(email=email, password=password)

        if user is not None:
            # Generate JWT tokens for Django API
            refresh = RefreshToken.for_user(user)
            django_tokens = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }

            # Generate a custom token for Firebase
            firebase_token_bytes = firebase_auth.create_custom_token(str(user.id))
            firebase_token = firebase_token_bytes.decode('utf-8') if isinstance(firebase_token_bytes, (bytes, bytearray)) else str(firebase_token_bytes)

            return Response({
                'django_tokens': django_tokens,
                'firebase_token': firebase_token
            })
        else:
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        

class GetUserView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'