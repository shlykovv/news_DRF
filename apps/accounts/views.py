from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login

from .models import CustomUser
from .serializers import (
    CustomUserRegistrationSerializer,
    CustomUserLoginSerializer,
    CustomUserUpdateSerializer,
    CustomUserProfileSerializer,
    ChangePasswordSerializer
)


class RegisterAPIView(generics.CreateAPIView):
    """Регистрация нового пользователя"""
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(request=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        refresh = RefreshToken.for_user(user)
        
        return Response({
            "user": CustomUserProfileSerializer(user).data,
            'refresh': str(refresh),
            "access": str(refresh.access_token),
            "message": "User registered successfull"
        }, status=status.HTTP_201_CREATED)


class LoginAPIView(generics.GenericAPIView):
    """Авторизация пользователя"""
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserLoginSerializer
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(request=request.data)
        serializer.is_valid(raise_exception=True)
        user = serialzier.validated_data.get("user")
        
        login(user)
        refresh = RefreshToken.for_user(user)
        
        return Response({
            "user": CustomUserProfileSerializer(user).data,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "message": "User login successfull",
        }, status=status.HTTP_200_OK)


class ProfileAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Просмотр и обновление профиля"""
    serializer_class = CustomUserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        if self.request.method == "PUT" or self.request.method == "PATCH":
            return CustomUserUpdateSerializer
        return CustomUserProfileSerializer


class ChangePasswordAPIView(generics.UpdateAPIView):
    """ Обновление пароля"""
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        serializer = self.get_serialzier(request=request.data)
        serializer.is_valid(raise_exceprion=True)
        serializer.save()
        
        return Response({
            "message": "Password changed successfull"
        }, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    """Выход пользователя"""
    try:
        refresh_token = request.data.get("refresh_token")
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        return Response({
            "message": "Logout successfull"
        }, status=status.HTTP_200_OK)
    except Exception:
        return Response({
            "error": "Invalid token."
        },status=status.HTTP_400_BAD_REQUEST)
