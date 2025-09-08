from rest_framework import generics, permissions, status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from django.shortcuts import get_object_or_404

from .models import Post, Category
from .serializers import (
    CategorySerializer,
    PostCreateUpdateSerializer,
    PostDetailSerializer,
    PostListSerializer
)

from .permissions import IsAuthorOrReadOnly


class CategoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "description"]
    ordering_fileds = ["name", "created_at"]
    ordering = ["name"]


class CategoryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """API endpoint для конкретной категории"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = "slug"


class PostListCreateAPIView(generics.ListCreateAPIView):
    """API endpoint для постов"""
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["category", "author", "status"]
    search_fields = ["title", "content"]
    ordering_fields = ["created_at", "updated_at", "views_count", "title"]
    ordering = ["-created_at"]
    
    def get_queryset(self):
        queryset = Post.objects.select_related("author", "category")
        
        # Фильтрация по правам доступа
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(status="PUBLISHED")
        else:
            queryset = queryset.filter(
                Q(status="PUBLISHED") | Q(author=self.request.user)
            )
        return queryset
    
    def get_serializer_class(self):
        if self.request.method == "POST":
            return PostCreateUpdateSerializer
        return PostListSerializer


class PostDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """API endpoint для конкретного поста"""
    queryset = Post.objects.select_related("author", "category")
    serializer_class = PostDetailSerializer
    permissions_classes = [IsAuthorOrReadOnly]
    lookup_field = "slug"
    
    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATH"]:
            return PostCreateUpdateSerializer
        return PostDetailSerializer
    
    def retrieve(self, request, *args, **kwargs):
        """Увеличивает счетчик просмотров при GET просмотрах"""
        instance = self.get_object()
        
        if request.method == "GET":
            instance.increments_views()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class MyPostAPIView(generics.ListAPIView):
    """API endpoint для постов текущего пользователя"""
    serializer_class = PostListSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["category", "status"]
    search_fields = ["name", "content"]
    ordering_fields = ["created_at", "updated_at", "views_count", "title"]
    ordering = ["-created_at"]
    
    def get_queryset(self):
        return Post.objects.filter(
            author=self.request.user
        ).select_related("author", "category")
        

@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def posts_by_category(request, category_slug):
    """Посты определенной категории"""
    category = get_object_or_404(Category, slug=category_slug)
    posts = Post.objects.filter(
        category=category,
        status="PUBLISHED").select_related(
            "author", "category").order_by("-created_at")
    serializer = PostListSerializer(posts, many=True, context={"request": request})
    return Response(
        {
            "category": CategorySerialzier(category).data,
            "posts": serializer.data
        }
    )


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def popular_posts(request):
    """10 популярных постов"""
    posts = Post.objects.filter(
        status="PUBLISHED"
    ).select_related("author", "category").order_by(["-views_count"])[:10]
    
    serializer = PostListSerializer(
        posts,
        many=True,
        context = {"request": request}
        )
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def recent_posts(request):
    """10 последних постов"""
    posts = Post.objects.filter(
        status="PUBLISHED"
    ).select_related("author", "category").order_by("-created_at")[:10]
    
    serializer = PostListSerializer(
        posts,
        many=True,
        context={"request": request}
    )
    return Response(serializer.data)
