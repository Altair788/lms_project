from django.contrib import admin
from .models import Course, Lesson, Subscription


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner', 'last_updated']
    search_fields = ['title', 'description']
    list_filter = ['owner', 'last_updated']


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'owner']
    search_fields = ['title', 'description', 'course__title']
    list_filter = ['course', 'owner']


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'course']
    search_fields = ['user__email', 'course__title']
    list_filter = ['course']
