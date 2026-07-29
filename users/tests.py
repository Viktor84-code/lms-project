from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class UserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create(
            email='test@test.com',
            first_name='Test',
            last_name='User',
            phone='123456789',
            city='Moscow'
        )
        user.set_password('testpass123')
        user.save()
        self.assertEqual(user.email, 'test@test.com')
        self.assertEqual(user.first_name, 'Test')
        self.assertTrue(user.check_password('testpass123'))

    def test_user_str_method(self):
        user = User.objects.create(email='str@test.com')
        self.assertEqual(str(user), 'str@test.com')

    def test_user_full_name(self):
        user = User.objects.create(
            email='full@test.com',
            first_name='Иван',
            last_name='Петров'
        )
        # если в модели есть метод get_full_name
        if hasattr(user, 'get_full_name'):
            self.assertEqual(user.get_full_name(), 'Иван Петров')
