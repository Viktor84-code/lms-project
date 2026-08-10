from datetime import timedelta

from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from lms.models import Course, Lesson, Subscription
from lms.serializers import CourseSerializer, LessonSerializer
from lms.tasks import send_course_update_email
from users.permissions import IsModer, IsOwner


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            # Создавать и удалять могут только не-модераторы
            self.permission_classes = [IsAuthenticated, ~IsModer]
        elif self.action in ['update', 'partial_update']:
            # Редактировать могут модераторы ИЛИ владельцы
            self.permission_classes = [IsAuthenticated, IsModer | IsOwner]
        else:
            # Просматривать могут модераторы ИЛИ владельцы
            self.permission_classes = [IsAuthenticated, IsModer | IsOwner]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        course = self.get_object()
        old_updated_at = course.updated_at
        serializer.save()

        # Доп. задание: проверка на 4 часа
        if old_updated_at:
            time_diff = timezone.now() - old_updated_at
            if time_diff > timedelta(hours=4):
                send_course_update_email.delay(course.id)
        else:
            # Если курс создан впервые (не должно быть, но на всякий случай)
            send_course_update_email.delay(course.id)


class LessonListCreateView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            # Создавать могут только не-модераторы
            self.permission_classes = [IsAuthenticated, ~IsModer]
        else:
            # Просматривать могут модераторы ИЛИ владельцы
            self.permission_classes = [IsAuthenticated, IsModer | IsOwner]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.request.method == 'DELETE':
            # Удалять могут только не-модераторы
            self.permission_classes = [IsAuthenticated, ~IsModer]
        elif self.request.method in ['PUT', 'PATCH']:
            # Редактировать могут модераторы ИЛИ владельцы
            self.permission_classes = [IsAuthenticated, IsModer | IsOwner]
        else:
            # Просматривать могут модераторы ИЛИ владельцы
            self.permission_classes = [IsAuthenticated, IsModer | IsOwner]
        return super().get_permissions()


class SubscriptionView(APIView):
    def post(self, request):
        user = request.user
        course_id = request.data.get('course_id')
        course = get_object_or_404(Course, id=course_id)

        subscription = Subscription.objects.filter(user=user, course=course)

        if subscription.exists():
            subscription.delete()
            message = 'Подписка удалена'
        else:
            Subscription.objects.create(user=user, course=course)
            message = 'Подписка добавлена'

        return Response({'message': message})


class PaymentStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, session_id):
        try:
            from lms.services import retrieve_checkout_session
            session = retrieve_checkout_session(session_id)
            return Response({
                'session_id': session_id,
                'status': session['payment_status'],
            })
        except Exception as e:
            return Response({'error': str(e)}, status=400)
