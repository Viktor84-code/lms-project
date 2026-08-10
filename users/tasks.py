from datetime import timedelta

from celery import shared_task
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


@shared_task
def block_inactive_users():
    """Блокировка пользователей, не заходивших более месяца"""
    month_ago = timezone.now() - timedelta(days=30)

    # Используем batch-обновление (не по одному!)
    count = User.objects.filter(
        last_login__lt=month_ago,
        is_active=True
    ).update(is_active=False)

    return f'Заблокировано {count} неактивных пользователей'
