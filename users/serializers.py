from rest_framework import serializers

from users.models import Payment, User


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    payments = serializers.PrimaryKeyRelatedField(
        many=True, required=False, queryset=Payment.objects.all()
    )
    password = serializers.CharField(write_only=True)  # Добавляем поле password

    def create(self, validated_data):
        payments = validated_data.pop(
            "payments", None)  # Извлекаем payments, если они есть
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()

        # Если есть платежи, добавляем их к пользователю
        if payments:
            user.payments.set(payments)

        return user

    class Meta:
        model = User
        fields = ("email", "phone", "city", "payments", "password",)