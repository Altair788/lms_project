from django.urls import reverse
from rest_framework import status

from rest_framework.test import APITestCase

from lms.models import Course, Lesson
from users.models import User


class LmsAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            email="admin@sky.pro"
        )
        self.course = Course.objects.create(
            title="test course",
            description="test description"
        )
        self.lesson = Lesson.objects.create(
            title="test lesson",
            course=self.course,
            owner=self.user
        )
        self.client.force_authenticate(user=self.user)


    def test_course_retrieve(self):
        url = reverse("lms:courses-detail", args=(self.course.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
