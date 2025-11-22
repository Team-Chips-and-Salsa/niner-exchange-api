from django.contrib.auth import authenticate
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from firebase_admin import auth as firebase_auth
from core.throttles import UserRateThrottle


class LoginView(APIView):
    throttle_classes = [UserRateThrottle]
    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response(
                {"error": "Email and password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(email=email, password=password)

        if user is not None:
            user.last_active = timezone.now()
            user.save(update_fields=['last_active'])
            refresh = RefreshToken.for_user(user)
            django_tokens = {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }

            firebase_token_bytes = firebase_auth.create_custom_token(str(user.id))
            firebase_token = (
                firebase_token_bytes.decode("utf-8")
                if isinstance(firebase_token_bytes, (bytes, bytearray))
                else str(firebase_token_bytes)
            )

            return Response(
                {"django_tokens": django_tokens, "firebase_token": firebase_token}
            )
        else:
            return Response(
                {"error": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )
