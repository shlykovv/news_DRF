from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password

from .models import CustomUser


class CustomUserRegistrationSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователя"""
    password = serializers.CharField(
        write_only=True,
        validators=[validate_password]
    )
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        fields = ("username", "email", "password", "password_confirm",
                  "first_name", "last_name")
    
    def validate(self, attrs):
        password = attrs.get("password")
        password_confirm = attrs.get("password_confirm")
        if password != password_confirm:
            raise serializers.ValidationError({
                "password": "Password fields didnt match."
            })
        return attrs
    
    def create(self, validated_data):
        validated_data.pop("password_confirm")
        user = CustomUser.objects.create_user(**validated_data)
        return user


class CustomUserSerializer(serializers.Serializer):
    """Сериализатор для входа пользователя"""
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        
        if email and password:
            user = authenticate(
                request=self.context.get("request"),
                username=email,
                password=password
            )
            if not user:
                raise serializers.ValidationError(
                    "User not found"
                )
            if not user.is_active:
                raise serializers.ValidationError(
                    "User account is disabled."
                )
            attrs["user"] = user
            return attrs
        else:
            raise serializers.ValidationError(
                "Must include 'email' and 'password'."
            )


class CustomUserProfileSerializer(serializers.ModelSerializer):
    """Сериализатор для профиля пользователя"""
    full_name = serializers.ReadOnlyField()
    posts_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    
    class Meta:
        model = CustomUser
        fields = (
            "id", "username", "email", "first_name", "last_name",
            "full_name", "avatar", "bio", "created_at", "updated_at",
            "posts_count", "comments_count"
        )
        read_only_fields = ("id", "created_at", "updated_at")
        
    def get_posts_count(self, obj):
        return obj.posts.count()
    
    def get_comments_count(self, obj):
        return obj.comments.count()


class CustomUserUpdateSerializer(serializers.ModelSerialzier):
    """Сериализатор для обновления профиля у пользователя"""
    
    class Meta:
        model = CustomUser
        fields = ("first_name", "last_name", "avatar", "bio",)
        
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class ChangePasswordSerializer(serializers.Serializer):
    """Сериализатор для смены пароля пользователя"""
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(
        required=True,
        validators=[validate_password]
    )
    new_password_confirm = serializers.CharField(required=True)
    
    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password incorrect.")
        return value
    
    def validate(self, attrs):
        password = attrs.get("new_password")
        new_password_confirm = attrs.get("new_password_confirm")
        if password != new_password_confirm:
            raise serializers.ValidationError(
                {"new_password": "Password fields didnt mutch."}
            )
        return attrs
    
    def save(self):
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save()
        return user
