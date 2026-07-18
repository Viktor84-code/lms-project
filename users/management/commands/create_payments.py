from django.core.management.base import BaseCommand

from lms.models import Course, Lesson
from users.models import Payment, User


class Command(BaseCommand):
    help = "Создаёт тестовые платежи"

    def handle(self, *args, **kwargs):
        # Берём первого пользователя (или создаём, если нет)
        user, _ = User.objects.get_or_create(email="test@test.com", defaults={"password": "123"})

        # Берём первый курс и урок
        course = Course.objects.first()
        lesson = Lesson.objects.first()

        # Создаём платежи
        Payment.objects.create(user=user, course=course, amount=1000.00, payment_method="cash")

        Payment.objects.create(user=user, lesson=lesson, amount=500.00, payment_method="transfer")

        self.stdout.write(self.style.SUCCESS("Тестовые платежи созданы!"))
