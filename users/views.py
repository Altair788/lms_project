from django_filters.rest_framework import DjangoFilterBackend
from requests import RequestException
from rest_framework import generics, status, viewsets
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from stripe import StripeError

from users.models import Payment, User
from users.serializers import PaymentSerializer, UserSerializer
from users.services import (convert_rub_to_usd, create_stripe_price,
                            create_stripe_product, create_stripe_session,
                            get_session_data)


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.save()


class UserListAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class UserRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


#  поддерживает как put так и putch
class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class UserDestroyAPIView(generics.DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = (
        "paid_course",
        "paid_lesson",
        "payment_method",
    )


class PaymentCreateAPIView(CreateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    def perform_create(self, serializer):
        payment_method = serializer.validated_data["payment_method"]
        course = serializer.validated_data["course"]
        amount = serializer.validated_data["payment_amount"]

        if payment_method == "card":
            try:
                product = create_stripe_product(course.title)
                amount_in_dollars = convert_rub_to_usd(amount)
                price = create_stripe_price(amount_in_dollars, product.id)
                session_id, payment_link = create_stripe_session(price)
                payment = serializer.save(user=self.request.user)
                payment.session_id = session_id
                payment.link = payment_link
                payment.save()
            except StripeError as se:
                return Response(
                    {"error": "Stripe error occurred", "details": str(se)},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            except RequestException as re:
                return Response(
                    {
                        "error": "Error occurred while converting currency",
                        "details": str(re),
                    },
                    status=status.HTTP_503_SERVICE_UNAVAILABLE,
                )

            except ValueError as ve:
                return Response(
                    {"error": "Invalid data provided", "details": str(ve)},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CheckoutSessionsRetrieveAPIView(RetrieveAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    def retrieve(self, request, *args, **kwargs):
        # Получаем объект Payment по session_id
        payment = self.get_object()

        try:
            # Получаем данные сессии из Stripe
            session_data = get_session_data(payment.session_id)

            if session_data:
                # Извлекаем статус платежа из данных сессии
                payment_status = session_data.get("payment_status", "pending")
                # Обновляем статус платежа в нашей базе данных
                payment.payment_status = payment_status
                payment.save()  # Сохраняем изменения

            # Сериализуем объект и возвращаем данные в ответе
            serializer = self.get_serializer(payment)
            return Response(serializer.data)

        except Payment.DoesNotExist:
            return Response({
                'error': 'Payment not found'
            }, status=status.HTTP_404_NOT_FOUND)

        except StripeError as se:
            return Response({
                'error': 'Stripe error occurred',
                'details': str(se)
            }, status=status.HTTP_400_BAD_REQUEST)

        except RequestException as re:
            return Response({
                'error': 'Error occurred while retrieving session data',
                'details': str(re)
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        except ValueError as ve:
            return Response({
                'error': 'Invalid data provided',
                'details': str(ve)
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
