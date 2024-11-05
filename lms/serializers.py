from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from lms.models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, source="lesson_set", required=False)
    count_lessons = SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"

    def get_count_lessons(self, course):
        return course.lesson_set.count()
