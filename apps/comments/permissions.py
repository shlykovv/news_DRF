from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Разрешение, позволяющее редактировать объект только автору"""
    
    def has_object_permission(self, request, view, obj):
        # Разрешение на чтение для всех
        if request.method in permissions.SAFE_METHODS:
            return True
        # Разрешение на запись только для автора
        return obj.author == request.user