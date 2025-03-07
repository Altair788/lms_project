from django.shortcuts import get_object_or_404
from rest_framework import generics, status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from lms.models import Course, Lesson, Subscription
from lms.paginations import LmsPaginator
from lms.serializers import (CourseSerializer, LessonSerializer,
                             SubscriptionSerializer)
from lms.tasks import send_update_notification
from users.permissions import IsModer, IsOwner


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = LmsPaginator

    def get_queryset(self):
        queryset = super().get_queryset()
        course_id = self.request.query_params.get("course_id")

        if course_id is not None:
            try:
                queryset = queryset.filter(course_id=int(course_id))
            except ValueError:
                # Обработка ошибки: неверный формат dog_id
                queryset = queryset.none()  # Возвращаем пустой QuerySet

        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.action in (
            "retrieve",
            "update",
            "partial_update",
        ):
            self.permission_classes = (
                IsAuthenticated,
                IsModer | IsOwner,
            )
        elif self.action == "create":
            self.permission_classes = (
                IsAuthenticated,
                ~IsModer,
            )
        elif self.action == "destroy":
            self.permission_classes = (
                IsAuthenticated,
                ~IsModer | IsOwner,
            )
        return super().get_permissions()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        send_update_notification.delay(instance.id)

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (
        ~IsModer,
        IsAuthenticated,
    )

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    pagination_class = LmsPaginator


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (
        IsAuthenticated,
        IsModer | IsOwner,
    )


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (
        IsAuthenticated,
        IsModer | IsOwner,
    )


class LessonDestroyAPIView(generics.DestroyAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (
        IsAuthenticated,
        ~IsModer | IsOwner,
    )


class SubscriptionAPIView(APIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [
        IsAuthenticated
    ]  # Убедитесь, что только аутентифицированные пользователи могут управлять подписками

    def post(self, request, course_id):
        user = request.user  # Получаем текущего пользователя

        # Получаем объект курса из базы данных
        course_item = get_object_or_404(Course, id=course_id)

        # Проверяем существование подписки для текущего пользователя и курса
        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            # Если подписка существует - удаляем ее
            subs_item.delete()
            message = "Подписка удалена"
        else:
            # Если подписки нет - создаем новую
            Subscription.objects.create(user=user, course=course_item)
            message = "Подписка добавлена"

        return Response({"message": message}, status=status.HTTP_200_OK)
