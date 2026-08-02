from unittest.mock import patch, MagicMock

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from lms.models import Course, Lesson
from lms.models import Subscription
from lms.services import create_product, create_price, create_checkout_session
from users.models import Payment

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


class StripeServicesTest(APITestCase):
    def setUp(self):
        self.product_data = {
            'id': 'prod_123',
            'name': 'Test Course',
            'description': 'Test Description'
        }
        self.price_data = {
            'id': 'price_123',
            'unit_amount': 100000,
            'currency': 'rub'
        }
        self.session_data = {
            'id': 'cs_test_123',
            'url': 'https://checkout.stripe.com/...'
        }

    @patch('stripe.Product.create')
    def test_create_product(self, mock_create):
        mock_create.return_value = MagicMock(**self.product_data)
        product = create_product('Test Course', 'Test Description')
        mock_create.assert_called_once_with(
            name='Test Course',
            description='Test Description',
            tax_code='txcd_10103001'
        )
        self.assertEqual(product.id, 'prod_123')

    @patch('stripe.Price.create')
    def test_create_price(self, mock_create):
        mock_create.return_value = MagicMock(**self.price_data)
        price = create_price('prod_123', 1000)
        mock_create.assert_called_once_with(
            product='prod_123',
            unit_amount=100000,
            currency='rub'
        )
        self.assertEqual(price.id, 'price_123')

    @patch('stripe.checkout.Session.create')
    def test_create_checkout_session(self, mock_create):
        mock_create.return_value = MagicMock(**self.session_data)
        session = create_checkout_session('price_123', 'http://success/', 'http://cancel/')
        mock_create.assert_called_once_with(
            line_items=[{'price': 'price_123', 'quantity': 1}],
            mode='payment',
            success_url='http://success/',
            cancel_url='http://cancel/',
            managed_payments={'enabled': True}
        )
        self.assertEqual(session.id, 'cs_test_123')


class CoursePaymentViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            email='payuser@test.com',
            first_name='Pay'
        )
        self.user.set_password('testpass123')
        self.user.save()

        self.course = Course.objects.create(
            title='Pay Course',
            description='Pay Description',
            owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    @patch('lms.services.create_product')
    @patch('lms.services.create_price')
    @patch('lms.services.create_checkout_session')
    def test_course_payment(self, mock_session, mock_price, mock_product):
        mock_product.return_value = MagicMock(id='prod_123')
        mock_price.return_value = MagicMock(id='price_123')
        mock_session.return_value = MagicMock(
            id='cs_test_123',
            url='https://checkout.stripe.com/...'
        )

        response = self.client.post(f'/api/courses/{self.course.id}/pay/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('payment_url', response.data)
        self.assertIn('session_id', response.data)
        self.assertEqual(Payment.objects.count(), 1)
