from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from .models import Course, Subscription


@shared_task
def send_course_update_email(course_id):
    """Отправка уведомлений подписчикам об обновлении курса"""
    try:
        course = Course.objects.get(id=course_id)
        subscribers = Subscription.objects.filter(course=course)

        emails = list(subscribers.values_list('user__email', flat=True))

        if emails:
            send_mail(
                subject=f'Обновление курса: {course.title}',
                message=f'Курс "{course.title}" был обновлен. Проверьте новые материалы!',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=emails,
                fail_silently=False,
            )
            return f'Отправлено {len(emails)} писем для курса {course.id}'
        return f'Нет подписчиков для курса {course.id}'
    except Course.DoesNotExist:
        return f'Курс {course_id} не найден'
