from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from lms.models import Course, Lesson


class CourseSerializer(serializers.ModelSerializer):
    count_lessons = SerializerMethodField()
    class Meta:
        model = Course
        fields = "__all__"

    def get_count_lessons(self, course):
        return course.lesson_set.count()


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = "__all__"