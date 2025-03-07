import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from lms.models import Course, Lesson
from users.models import User


class CourseAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="admin@sky.pro")
        self.course = Course.objects.create(
            title="test course", description="test description", owner=self.user
        )
        self.lesson = Lesson.objects.create(
            title="test lesson", course=self.course, owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_course_retrieve(self):
        url = reverse("lms:courses-detail", args=(self.course.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(data.get("title"), self.course.title)

    def test_course_create(self):
        url = reverse("lms:courses-list")
        data = {"title": "Python beginners course"}
        response = self.client.post(url, data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.all().count(), 2)

    def test_course_update(self):
        url = reverse("lms:courses-detail", args=(self.course.pk,))
        data = {"title": "Java beginners course"}
        response = self.client.patch(url, data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), "Java beginners course")

    def test_course_delete(self):
        url = reverse("lms:courses-detail", args=(self.course.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.all().count(), 0)

    def test_course_list(self):
        url = reverse("lms:courses-list")
        response = self.client.get(url)
        # pretty_json = json.dumps(response.json(), indent=4, sort_keys=True)
        # print(pretty_json)

        data = response.json()

        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "count_lessons": 1,
                    "description": self.course.description,
                    "id": self.course.pk,
                    "isSubscribed": False,
                    "lessons": [
                        {
                            "course": self.course.pk,
                            "description": self.lesson.description,
                            "id": self.lesson.pk,
                            "linkVideo": self.lesson.link_video,
                            "owner": self.user.pk,
                            "preview": self.lesson.preview,
                            "title": self.lesson.title,
                        }
                    ],
                    "owner": self.user.pk,
                    "preview": None,
                    "title": self.course.title,
                }
            ],
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("Actual data:", json.dumps(data, indent=2))
        print("Expected data:", json.dumps(result, indent=2))
        self.assertEqual(data, result)


class SubscriptionsAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="admin@sky.pro")
        self.course = Course.objects.create(
            title="test course", description="test description", owner=self.user
        )
        self.lesson = Lesson.objects.create(
            title="test lesson", course=self.course, owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_subscriptions_manage(self):
        url = reverse("lms:subscriptions-manage", args=(self.course.pk,))
        response = self.client.post(url, content_type="application/json")
        # pretty_json = json.dumps(response.json(), indent=4, sort_keys=True)
        # print(pretty_json)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("message"), "Подписка добавлена")


class LessonAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="admin@sky.pro")
        self.course = Course.objects.create(
            title="test course", description="test description", owner=self.user
        )
        self.lesson = Lesson.objects.create(
            title="test lesson",
            course=self.course,
            owner=self.user,
            link_video="https://www.youtube.com/live/uNLIusFdnj8?si=6w0CzMmMPdRBIO3T",
        )
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        url = reverse("lms:lessons-retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(data.get("title"), self.lesson.title)

    def test_lesson_create(self):
        url = reverse("lms:lessons-create")
        data = {"title": "lesson 1", "course": self.course.pk}
        response = self.client.post(url, data=json.dumps(data),  content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_update(self):
        url = reverse("lms:lessons-update", args=(self.course.pk,))
        data = {
            "title": "lesson 2",
        }
        response = self.client.patch(url, data=json.dumps(data), content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), "lesson 2")

    def test_incorrect_link_video_update(self):
        url = reverse("lms:lessons-update", args=(self.lesson.pk,))
        data = {
            "link_video": "https://yandex.ru/video/search?text=%D0%B2%D0%B8%D0%B4%D0%B5%D0%BE",
        }
        response = self.client.patch(url, data=json.dumps(data), content_type="application/json")

        # pretty_json = json.dumps(response.json(), indent=4, sort_keys=True)
        # print(pretty_json)

        result = response.json()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # self.assertEqual(
        #     result.get("link_video"), ["Допускается ссылка только на youtube.com."]
        # )
        self.assertEqual(response.data['link_video'], ['Допускается ссылка только на youtube.com.'])

    def test_lesson_delete(self):
        url = reverse("lms:lessons-delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_list(self):
        url = reverse("lms:lessons-list")
        response = self.client.get(url)
        # pretty_json = json.dumps(response.json(), indent=4, sort_keys=True)
        # print(pretty_json)

        data = response.json()

        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "course": self.course.pk,
                    "description": self.lesson.description,
                    "id": self.lesson.pk,
                    "linkVideo": self.lesson.link_video,
                    "owner": self.user.pk,
                    "preview": None,
                    "title": self.lesson.title,
                }
            ],
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)
