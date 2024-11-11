from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from lms.models import Course, Lesson, Subscription
from lms.validators import validate_key_words


class LessonSerializer(serializers.ModelSerializer):
    link_video = serializers.CharField(validators=[validate_key_words], required=False)

    class Meta:
        model = Lesson
        fields = "__all__"


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, source="lesson_set", required=False)
    count_lessons = SerializerMethodField()
    is_subscribed = SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"

    def get_count_lessons(self, course):
        return course.lesson_set.count()

    def get_is_subscribed(self, course):
        request = self.context.get("request")
        if not request.user.is_authenticated:
            return False
        return Subscription.objects.filter(user=request.user, course=course).exists()
