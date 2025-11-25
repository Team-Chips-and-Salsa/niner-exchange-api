from rest_framework import permissions, status
from rest_framework.views import APIView
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from core.models import CustomUser
from firebase_admin import auth as firebase_auth


# Used AI to figure out how to verify email upon registration
class VerifyEmailView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.is_verified_student = True
            user.save()

            refresh = RefreshToken.for_user(user)
            django_tokens = {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }

            firebase_token_bytes = firebase_auth.create_custom_token(str(user.id))
            firebase_token = firebase_token_bytes.decode("utf-8")

            return Response(
                {
                    "message": "Email verified successfully! You are now logged in.",
                    "django_tokens": django_tokens,
                    "firebase_token": firebase_token,
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error": "Invalid verification link."},
                status=status.HTTP_400_BAD_REQUEST,
            )
