from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from .models import Product, Stock
from .serializers import ProductSerializer, StockSerializer


class ProductViewSet(ModelViewSet):
    """ViewSet для продукта."""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # Пагинация настраивается в settings.py
    filter_backends = [DjangoFilterBackend, SearchFilter]
    # Поля для фильтрации (если нужно, например, ?title=название)
    filterset_fields = ['title']
    # Поля для поиска (работает с ?search=...)
    search_fields = ['title', 'description']


class StockViewSet(ModelViewSet):
    """ViewSet для склада."""
    queryset = Stock.objects.all().prefetch_related('positions__product') # Оптимизация запроса
    serializer_class = StockSerializer
    # Пагинация настраивается в settings.py
    filter_backends = [DjangoFilterBackend, SearchFilter]
    # Фильтрация по ID продукта в позициях склада: ?positions__product__id=1
    filterset_fields = ['positions__product__id']
    # Поиск по названию или описанию продукта в позициях склада: ?search=помид
    # Это реализует дополнительное задание
    search_fields = ['positions__product__title', 'positions__product__description']