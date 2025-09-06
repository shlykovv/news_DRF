from django.urls  import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

app_name = "users"

urlpatterns = [
    path("register/", views.RegisterAPIView.as_view(), name="register"),
    path("login/", views.LoginAPIView.as_view(), name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.ProfileAPIView.as_view(), name="profile"),
    path("change-password/", views.ChangePasswordAPIView.as_view(), name="change_password"),
    path("refresh-token/", TokenRefreshView.as_view(), name="token_refresh"),
]