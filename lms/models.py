from django.conf import settings
from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=200)
    preview = models.ImageField(upload_to="courses/", blank=True, null=True)
    description = models.TextField()
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='courses',
        verbose_name='Владелец'
    )
    price = models.DecimalField(  # <-- ДОБАВИТЬ ЭТО
        max_digits=10,
        decimal_places=2,
        default=1000,
        verbose_name='Цена'
    )

    def __str__(self):
        return self.title


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
    title = models.CharField(max_length=200)
    description = models.TextField()
    preview = models.ImageField(upload_to="lessons/", blank=True, null=True)
    video_url = models.URLField()
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='lessons',
        verbose_name='Владелец'
    )

    def __str__(self):
        return self.title


class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subscriptions')
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='subscriptions')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'course')
