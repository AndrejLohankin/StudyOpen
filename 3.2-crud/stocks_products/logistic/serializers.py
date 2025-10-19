from rest_framework import serializers
from .models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор для продукта."""
    class Meta:
        model = Product
        fields = ['id', 'title', 'description']


class ProductPositionSerializer(serializers.ModelSerializer):
    """Сериализатор для позиции продукта на складе."""
    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']

    def to_representation(self, instance):
        """Переопределяем, чтобы в ответе были данные продукта, а не просто его ID."""
        representation = super().to_representation(instance)
        # Добавляем данные о продукте внутрь позиции
        product_representation = ProductSerializer(instance.product).data
        representation['product'] = product_representation
        return representation


class StockSerializer(serializers.ModelSerializer):
    """Сериализатор для склада."""
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ['id', 'address', 'positions']

    def create(self, validated_data):
        """Создание склада и его позиций."""
        # Извлекаем позиции из валидированных данных
        positions_data = validated_data.pop('positions')
        # Создаем сам склад
        stock = Stock.objects.create(**validated_data)

        # Создаем позиции для склада
        for position_data in positions_data:
            StockProduct.objects.create(stock=stock, **position_data)

        return stock

    def update(self, instance, validated_data):
        """Обновление склада и его позиций."""
        # Извлекаем позиции из валидированных данных
        positions_data = validated_data.pop('positions', None)

        # Обновляем основные поля склада
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Обновляем позиции склада, если они были переданы
        if positions_data is not None:
            for position_data in positions_data:
                product = position_data.get('product')
                quantity = position_data.get('quantity')
                price = position_data.get('price')

                # Используем update_or_create для обновления или создания позиции
                StockProduct.objects.update_or_create(
                    stock=instance,
                    product=product,
                    defaults={'quantity': quantity, 'price': price}
                )

        return instance
