import os

from rest_framework import permissions, generics, status
from rest_framework.response import Response
from core.models.user import CustomUser
from core.serializers.user_serializer import RegisterSerializer
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.conf import settings

FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

    # Used AI to figure out how to send verification email upon registration
    def perform_create(self, serializer):
        user = serializer.save()
        try:
            token = default_token_generator.make_token(user)
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            verification_link = f"{FRONTEND_URL}/verify-email/{uidb64}/{token}/"

            subject = "Verify Your Niner Exchange Account"
            message = (
                f"Hi {user.first_name},\n\n"
                f"Welcome to Niner Exchange! Please click the link below to verify your account:\n\n"
                f"{verification_link}\n\n"
                "Go Niners!"
            )

            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
        except Exception as e:
            user.delete()
            raise e

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        try:
            self.perform_create(serializer)
        except Exception as e:
            return Response(
                {
                    "error": f"Registration failed. Could not send verification email. {str(e)}"
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(
            {
                "message": "Registration successful! Please check your @charlotte.edu email to verify your account."
            },
            status=status.HTTP_201_CREATED,
        )
