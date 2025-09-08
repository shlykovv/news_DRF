from rest_framework import serializers

from .models import Comment
from apps.main.models import Post
from .utils import validate_comment_check



class CommentSerializer(serializers.ModelSerializer):
    """Базовый сериализатор для комментариев"""
    author_info = serializers.SerializerMethodField()
    replies_count = serializers.ReadOnlyField()
    is_reply = serializers.ReadOnlyField()
    
    class Meta:
        model = Comment
        fields = ("id", "content", "author", "author_info", "parent",
                  "is_active", "replies_count", "is_reply",
                  "created_at", "updated_at")
        read_only_fileds = ("author", "is_active", "created_at")
    
    def get_author_info(self, obj):
        author = obj.author
        return {
            "id": author.id,
            "username": author.username,
            "fullname": author.fullname,
            "avatar": author.avatar.url if author.avatar else None
        }


class CommentCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания комментариев"""
    
    class Meta:
        model = Comment
        fields = ("post", "parent", "content")
    
    def validate_content(self, value):
        validate_comment_check(value)
        return value

    def validate_post(self, value):
        if not Post.objects.filter(id=value.id, status="PUBLISHED").exists():
            raise serializers.ValidationError(
                "Post not found."
            )
        return value
    
    def validate_parent(self, value):
        if value and value.post != self.initial_data.get("post"):
            raise serializers.ValidationError(
                "Parent comment must belong to the same post.")
        return value
    
    def create(self, validated_data):
        validated_data["author"] = self.context["request"].user
        return super().create(validated_data)


class CommentUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для обновления комментариев"""
    
    class Meta:
        model = Comment
        fields = ("content",)
    
    def validate_content(self, value):
        validate_comment_check(value)
        return value


class CommentDetailSerializer(serializers.ModelSerializer):
    """Детальный сериализатор комментария с ответами"""
    replies = serializers.SerializerMethodField()
    
    class Meta:
        fields = CommentSerializer.Meta.fields + ("replies",)
    
    def get_replies(self, obj):
        if obj.parent is None: # Показываем ответы только для основных комментариев
            replies = obj.replies.filter(is_active=True).order_by("created_at")
            return CommentSerializer(replies, many=True, context=self.context).data
        return []
