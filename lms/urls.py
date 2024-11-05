from django.urls import path
from rest_framework.routers import DefaultRouter

from lms.apps import LmsConfig
from lms.views import (CourseViewSet, LessonCreateAPIView,
                       LessonDestroyAPIView, LessonListAPIView,
                       LessonRetrieveAPIView, LessonUpdateAPIView)

app_name = LmsConfig.name

router = DefaultRouter()
router.register(r"courses", CourseViewSet, basename="courses")

urlpatterns = [
    path("lessons/", LessonListAPIView.as_view(), name="lessons-list"),
    path("lessons/create/", LessonCreateAPIView.as_view(), name="lessons-create"),
    path("lessons/<int:pk>/", LessonRetrieveAPIView.as_view(), name="lessons-retrieve"),
    path(
        "lessons/update/<int:pk>/", LessonUpdateAPIView.as_view(), name="lessons-update"
    ),
    path(
        "lessons/delete/<int:pk>/",
        LessonDestroyAPIView.as_view(),
        name="lessons-delete",
    ),
] + router.urls
