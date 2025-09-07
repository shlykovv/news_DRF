from rest_framework import generics, permissions, status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from django.shortcuts import get_object_or_404

from .models import Post, Category
from .serializers import (
    CategorySerialzier,
    PostCreateUpdateSerializer,
    PostDetailSerializer,
    PostListSerializer
)

from .permissions import IsAuthorOrReadOnly


class CategoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerialzier
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "description"]
    ordering_fileds = ["name", "created_at"]
    ordering = ["name"]


class CategoryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """API endpoint для конкретной категории"""
    queryset = Category.objects.all()
    serializer_class = CategorySerialzier
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = "slug"


class PostListCreateAPIView(generics.ListCreateAPIView):
    """API endpoint для постов"""
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    permission_classes = [permission_classes.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["category", "author", "status"]
    search_fields = ["title", "content"]
    ordering_fields = ["created_at", "updated_at", "views_count", "title"]
    ordering = ["-created_at"]
    
    def get_queryset(self):
        queryset = Post.objects.select_related("author", "category")
    
