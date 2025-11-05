from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Разрешение, позволяющее редактировать или удалять только автору объекта.
    Для остальных пользователей доступны только чтение.
    """

    def has_object_permission(self, request, view, obj):
        # Разрешаем все безопасные методы (GET, HEAD, OPTIONS) для всех
        if request.method in permissions.SAFE_METHODS:
            return True

        # Разрешаем редактирование и удаление только владельцу
        return obj.creator == request.user