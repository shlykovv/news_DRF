from django.urls import path

from . import views

app_name = "posts"

urlpatterns = [
    # Categories
    path("categories/", views.CategoryListCreateAPIView.as_view(), name="category-list"),
    path("categories/<slug:slug>/", views.CategoryDetailAPIView.as_view(), name="category-detail"),
    path("categories/<slug:category_slug>/posts/", views.posts_by_category, name="post-by-category"),
    
    # Post
    path("", views.PostListCreateAPIView.as_view(), name="post-list"),
    path("my-posts/", views.MyPostAPIView.as_view(), name="my-posts"),
    path("popular/", views.popular_posts, name="popular-post"),
    path("recent/", views.recent_posts, name="recent-posts"),
    path("<slug:slug>/", views.PostDetailAPIView.as_view(), name="post-detail")
]
