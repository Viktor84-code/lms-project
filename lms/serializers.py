from rest_framework import serializers

from lms.models import Subscription
from lms.validators import validate_youtube_url
from .models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    video_url = serializers.URLField(validators=[validate_youtube_url])

    class Meta:
        model = Lesson
        fields = '__all__'
        read_only_fields = ['owner']


class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    lessons_count = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()  # <-- ДОБАВИТЬ

    class Meta:
        model = Course
        fields = ['id', 'title', 'preview', 'description', 'owner', 'lessons', 'lessons_count',
                  'is_subscribed']  # <-- ДОБАВИТЬ is_subscribed
        read_only_fields = ['id', 'owner', 'lessons', 'lessons_count', 'is_subscribed']  # <-- ДОБАВИТЬ is_subscribed

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Subscription.objects.filter(user=request.user, course=obj).exists()
        return False
