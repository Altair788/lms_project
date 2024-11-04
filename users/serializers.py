from rest_framework import serializers

from users.models import User, Payment




class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = "__all__"

# class UserSerializer(serializers.ModelSerializer):
#     payments = PaymentSerializer(many=True, source='payment_set')
#     class Meta:
#         model = User
#         fields = "__all__"

class UserSerializer(serializers.ModelSerializer):
    payments = serializers.PrimaryKeyRelatedField(many=True, required=False, queryset=Payment.objects.all())

    class Meta:
        model = User
        fields = ['email', 'password', 'phone', 'city', 'payments']
        extra_kwargs = {
            'password': {'write_only': True},  # Пароль только для записи
        }

    def create(self, validated_data):
        payments = validated_data.pop('payments', None)  # Извлекаем payments, если они есть
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()

        # Если есть платежи, добавляем их к пользователю
        if payments:
            user.payments.set(payments)

        return user
