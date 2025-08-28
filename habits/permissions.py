from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """Пользовательское разрешение, разрешающее владельцу только доступ."""

    def has_object_permission(self, request, view, obj):
        # Проверка, является ли пользователь владельцем объекта
        return obj.owner == request.user
