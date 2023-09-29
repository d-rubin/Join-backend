from django.core import mail
from rest_framework.test import APITestCase
from django.contrib.auth.models import User


class LoginViewTest(APITestCase):
    def set_up_user(self):
        self.username = 'daniel'
        self.password = 'danieldr4.'
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def test_invalid_credentials(self):
        self.set_up_user()
        url = '/auth/login/'
        data = {
            'username': 'daniel',
            'password': 'daniel'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 401)

    def test_valid_credentials(self):
        self.set_up_user()
        url = '/auth/login/'
        data = {
            'username': 'daniel',
            'password': 'danieldr4.'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('token', response.data)


class RegisterViewTest(APITestCase):
    def test_successful_registration(self):
        url = '/auth/register/'
        data = {
            'email': 'test@example.com',
            'name': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('token', response.data)

    def test_existing_email(self):
        User.objects.create_user(username='existinguser', email='test@example.com', password='testpassword')
        url = '/auth/register/'
        data = {
            'email': 'test@example.com',
            'name': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 401)

    def test_existing_name(self):
        User.objects.create_user(username='testuser', email='existing@example.com', password='testpassword')
        url = '/auth/register/'
        data = {
            'email': 'test@example.com',
            'name': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['message'], 'Name already in use')

    def test_missing_fields(self):
        url = '/auth/register/'
        data = {
            'email': 'test@example.com',
            'name': 'testuser'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 401)


class ResetPasswordViewTest(APITestCase):
    def setUp(self):
        self.email = 'test@example.com'
        self.user = User.objects.create_user(username='testuser', email=self.email, password='testpassword')

    def test_reset_password_email_sent(self):
        url = '/auth/reset-password/'
        data = {
            'email': self.email
        }
        with self.assertLogs('django.core.mail', level='INFO') as mail_logs:
            response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'Reset password email sent.')
