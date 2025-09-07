from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse


class Category(models.Model):
    """Модель категорий для постов блога"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = "categories"
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ("-created_at",)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Post(models.Model):
    """Модель постов"""
    STATUS_CHOICES = (("DRAFT", "Draft"), ("PUBLISHED", "Published"))
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    constent = models.TextField()
    image = models.ImageField(upload_to="posts/", blank=True, null=True)
    categories = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="posts"
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts"
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="PUBLISHED"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views_count = models.PositiveIntegerField(default=0)
    
    class Meta:
        db_table = "posts"
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        ordering = ("-created_at",)
        indexes = (
            models.Index(fields=("-created_at",)),
            models.Index(fields=("status", "created_at")),
            models.Index(fields=("categories", "-created_at")),
            models.Index(fields=("author", "-created_at"))
        )
        
        def __str__(self):
            return self.title
        
        def save(self, *args, **kwargs):
            if not self.slug:
                self.slug = slugify(self.title)
            super().save(*args, **kwargs)
        
        def get_absolute_url(self):
            return reverse("post-detail", kwargs={"slug": self.slug})
        
        @property
        def comments_count(self):
            """Количество комментариев к посту"""
            return self.comments.filter(is_active=True).count()
        
        def increment_views(self):
            """Увеличиваем счетчик просмотров"""
            self.views_count += 1
            self.save(update_fields=["views_count"])
        
        
