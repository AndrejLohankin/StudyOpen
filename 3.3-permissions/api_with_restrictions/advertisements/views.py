# views.py

from django.shortcuts import render
from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from django.core.exceptions import PermissionDenied
from advertisements.models import Advertisement, AdvertisementStatusChoices, Favorite
from advertisements.serializers import AdvertisementSerializer, UserSerializer
from advertisements.filters import AdvertisementFilter # Убедитесь, что импортировали
from rest_framework.permissions import BasePermission


def index(request):
    """Отображает главную страницу."""
    return render(request, 'advertisements/index.html')

class IsOwnerOrAdminOrReadOnly(BasePermission):
    """
    Разрешение, позволяющее:
    - Админу (is_staff) редактировать/удалять любое объявление.
    - Автору (creator) редактировать/удалять своё объявление.
    - Всем остальным только читать (GET, HEAD, OPTIONS).
    """

    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        if request.user.is_staff:
            return True
        return obj.creator == request.user


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    serializer_class = AdvertisementSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        permission_classes = []
        if self.action in ["create"]:
            permission_classes = [IsAuthenticated]
        elif self.action in ["update", "partial_update", "destroy"]:
            permission_classes = [IsAuthenticated, IsOwnerOrAdminOrReadOnly]
        else:
            permission_classes = [perm for perm in self.permission_classes]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """
        Ограничиваем доступ к объявлениям в зависимости от аутентификации и статуса,
        а затем применяем фильтры из запроса вручную.
        """
        user = self.request.user
        base_queryset = Advertisement.objects.all()
        if user.is_authenticated:
            queryset = base_queryset.filter(
                Q(status__in=[AdvertisementStatusChoices.OPEN, AdvertisementStatusChoices.CLOSED]) |
                Q(creator=user, status=AdvertisementStatusChoices.DRAFT)
            )
        else:
            queryset = base_queryset.filter(status__in=[AdvertisementStatusChoices.OPEN, AdvertisementStatusChoices.CLOSED])

        query_params = self.request.query_params
        status_param = query_params.get('status')
        if status_param:
            queryset = queryset.filter(status=status_param)

        creator_param = query_params.get('creator')
        if creator_param:
            try:
                creator_id = int(creator_param)
                queryset = queryset.filter(creator_id=creator_id)
            except (ValueError, TypeError):
                pass

        created_after = query_params.get('created_at_after')
        created_before = query_params.get('created_at_before')
        if created_after:
            queryset = queryset.filter(created_at__date__gte=created_after)
        if created_before:
            queryset = queryset.filter(created_at__date__lte=created_before)

        return queryset


    def perform_create(self, serializer):
        """Устанавливаем текущего пользователя как создателя объявления."""
        serializer.save(creator=self.request.user)

    def destroy(self, request, *args, **kwargs):
        """
        Валидация удаления чужого объявления внутри метода.
        (Второй вариант, как указано в задании - использовать IsOwnerOrAdminOrReadOnly в get_permissions)
        Для согласованности с первым вариантом разрешений, этот метод можно оставить как есть
        или удалить, так как проверка уже происходит через get_permissions.
        """
        instance = self.get_object()
        if instance.creator != request.user and not request.user.is_staff:
            raise PermissionDenied("Вы не можете удалить это объявление.")
        return super().destroy(request, *args, **kwargs)


    @action(detail=True, methods=['post'])
    def favorite(self, request, pk=None):
        """Добавить объявление в избранное."""
        advertisement = self.get_object()

        if not request.user.is_authenticated:
            return Response({"error": "Аутентификация обязательна для добавления в избранное."},
                            status=status.HTTP_401_UNAUTHORIZED)

        if advertisement.creator == request.user:
            return Response({"error": "Нельзя добавить своё объявление в избранное."},
                            status=status.HTTP_400_BAD_REQUEST)

        favorite, created = Favorite.objects.get_or_create(
            user=request.user,
            advertisement=advertisement
        )

        if created:
            return Response({"message": "Объявление добавлено в избранное."}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Объявление уже в избранном."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['delete'])
    def unfavorite(self, request, pk=None):
        """Удалить объявление из избранного."""
        advertisement = self.get_object()

        if not request.user.is_authenticated:
            return Response({"error": "Аутентификация обязательна для удаления из избранного."},
                            status=status.HTTP_401_UNAUTHORIZED)

        try:
            favorite = Favorite.objects.get(user=request.user, advertisement=advertisement)
            favorite.delete()
            return Response({"message": "Объявление удалено из избранного."}, status=status.HTTP_204_NO_CONTENT)
        except Favorite.DoesNotExist:
            return Response({"error": "Объявление не найдено в избранном."}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def favorites(self, request):
        """Получить список избранных объявлений текущего пользователя."""
        if not request.user.is_authenticated:
            return Response({"error": "Аутентификация обязательна для просмотра избранного."},
                            status=status.HTTP_401_UNAUTHORIZED)

        favorite_ads_ids = Favorite.objects.filter(user=request.user).values_list('advertisement_id', flat=True)
        queryset = self.get_queryset().filter(id__in=favorite_ads_ids)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def my_drafts(self, request):
        """Получить список черновиков текущего пользователя."""
        if not request.user.is_authenticated:
            return Response({"error": "Аутентификация обязательна для просмотра черновиков."},
                            status=status.HTTP_401_UNAUTHORIZED)

        queryset = self.get_queryset().filter(creator=request.user, status=AdvertisementStatusChoices.DRAFT)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
