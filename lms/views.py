from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated

from lms.models import Course, Lesson
from lms.serializers import CourseSerializer, LessonSerializer
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
