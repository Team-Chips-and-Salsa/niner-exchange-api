from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from core.views.auth_views.login_view import LoginView
from core.views.auth_views.logout_view import LogoutView
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
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("get-me/", GetMeView.as_view(), name="get-me"),
]
