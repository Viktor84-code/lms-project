from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from lms.models import Course, Lesson
from lms.models import Subscription

User = get_user_model()


class LessonAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            email='testuser@test.com',
            first_name='Test'
        )
        self.user.set_password('testpass123')
        self.user.save()

        self.course = Course.objects.create(
            title='Test Course',
            description='Test Description',
            owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_create_lesson(self):
        url = '/api/lessons/'
        data = {
            'course': self.course.id,
            'title': 'Test Lesson',
            'description': 'Lesson Description',
            'video_url': 'https://www.youtube.com/watch?v=abc123'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 1)

    def test_create_lesson_invalid_url(self):
        url = '/api/lessons/'
        data = {
            'course': self.course.id,
            'title': 'Invalid Lesson',
            'description': 'Description',
            'video_url': 'https://rutube.ru/video/123'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('video_url', response.data)

        def test_update_lesson(self):
            lesson = Lesson.objects.create(
                course=self.course,
                title='Old Title',
                description='Old Description',
                video_url='https://www.youtube.com/watch?v=old',
                owner=self.user
            )
            url = f'/api/lessons/{lesson.id}/'
            data = {'title': 'New Title'}
            response = self.client.patch(url, data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            lesson.refresh_from_db()
            self.assertEqual(lesson.title, 'New Title')

        def test_delete_lesson(self):
            lesson = Lesson.objects.create(
                course=self.course,
                title='To Delete',
                description='To Delete',
                video_url='https://www.youtube.com/watch?v=delete',
                owner=self.user
            )
            url = f'/api/lessons/{lesson.id}/'
            response = self.client.delete(url)
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
            self.assertEqual(Lesson.objects.count(), 0)

        def test_cannot_delete_others_lesson(self):
            other_user = User.objects.create(
                email='other@test.com',
                first_name='Other'
            )
            other_user.set_password('testpass')
            other_user.save()

            lesson = Lesson.objects.create(
                course=self.course,
                title='Other Lesson',
                description='Other Description',
                video_url='https://www.youtube.com/watch?v=other',
                owner=other_user
            )
            url = f'/api/lessons/{lesson.id}/'
            response = self.client.delete(url)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class SubscriptionAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            email='subuser@test.com',
            first_name='Sub'
        )
        self.user.set_password('testpass123')
        self.user.save()
        self.course = Course.objects.create(
            title='Course for Sub',
            description='Description',
            owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_subscribe(self):
        url = '/api/subscribe/'
        data = {'course_id': self.course.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Подписка добавлена')
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())

    def test_unsubscribe(self):
        Subscription.objects.create(user=self.user, course=self.course)
        url = '/api/subscribe/'
        data = {'course_id': self.course.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Подписка удалена')
        self.assertFalse(Subscription.objects.filter(user=self.user, course=self.course).exists())
