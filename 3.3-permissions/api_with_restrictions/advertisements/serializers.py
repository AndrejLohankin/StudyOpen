# serializers.py

from django.contrib.auth.models import User
from rest_framework import serializers
from advertisements.models import Advertisement, AdvertisementStatusChoices, Favorite # Импортируем Favorite


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at', 'updated_at') # Включаем updated_at

    def create(self, validated_data):
        """Метод для создания"""
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""
        request = self.context.get('request')

        # Проверка лимита открытых объявлений при создании или изменении статуса на OPEN
        if request and request.method in ["POST", "PUT", "PATCH"]:
            current_status = self.instance.status if self.instance else None
            new_status = data.get('status', current_status)

            if new_status == AdvertisementStatusChoices.OPEN:
                # Если статус меняется на OPEN или это создание нового с OPEN
                # и это не текущее объявление (т.е. не уменьшаем счётчик при закрытии другого)
                if not self.instance or self.instance.status != AdvertisementStatusChoices.OPEN:
                    open_ads_count = Advertisement.objects.filter(
                        creator=request.user,
                        status=AdvertisementStatusChoices.OPEN
                    ).exclude(id=self.instance.id if self.instance else None).count()

                    if open_ads_count >= 10:
                        raise serializers.ValidationError("У вас не может быть больше 10 открытых объявлений.")

        return data
