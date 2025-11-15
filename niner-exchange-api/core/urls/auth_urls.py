from django.urls import path

from core.views.auth_views.login_view import LoginView
from core.views.auth_views.register_view import RegisterView
from core.views.auth_views.verify_email_view import VerifyEmailView
from core.views.user_view import GetMeView

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path(
        "verify-email/<str:uidb64>/<str:token>/",
        VerifyEmailView.as_view(),
        name="verify-email",
    ),
    path("get-me/", GetMeView.as_view(), name="get-me"),
]
