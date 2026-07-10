from rest_framework.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from api.auth.views import RegisterUserView, LoginView, LogOutView

urlpatterns = [
    path("login", LoginView.as_view(), name="login_view"),
    path("token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("logout", LogOutView.as_view(), name="logout"),
    path("register/", RegisterUserView.as_view(), name="register_user"),
]