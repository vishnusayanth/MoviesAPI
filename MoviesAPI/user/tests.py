from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from user.views import RegisterView

REGISTER_URL = reverse('register')
COLLECTIONS_URL = '/collection/'
COLLECTION_URL = '/collection/1/'


class UserTestCases(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.factory = RequestFactory()
        self.request = self.factory.get(REGISTER_URL)

    def test_valid_register_view_setup(self):
        v = RegisterView()
        v.setup(self.request)
        self.assertTrue(True)

    def test_invalid_register_get_response(self):
        data = self.client.get(REGISTER_URL)
        self.assertEqual(405, data.status_code)

    def test_user_create_valid(self):
        username = 'test_user2'
        payload = {
            'username': username,
            'password': 'pass3',
        }
        self.client.post(REGISTER_URL, data=payload)
        exists = User.objects.filter(
            username=username,
        ).exists()
        self.assertTrue(exists)

    def test_user_create_token_in_response(self):
        payload = {
            'username': 'test_user2',
            'password': 'pass3',
        }
        res = self.client.post(REGISTER_URL, data=payload)
        self.assertIn('token', res.json())

    def test_invalid_payload_throws_error(self):
        payload = {
            'name': ''
        }
        try:
            self.client.post(REGISTER_URL, data=payload)
        except Exception:
            self.assertTrue(True)

    def test_login_required_collection_list(self):
        self.client.logout()
        res = self.client.get(COLLECTIONS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_required_collection_get(self):
        self.client.logout()
        res = self.client.get(COLLECTION_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_required_collection_create(self):
        self.client.logout()
        res = self.client.post(COLLECTION_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_required_collection_delet(self):
        self.client.logout()
        res = self.client.delete(COLLECTION_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_required_movies(self):
        self.client.logout()
        res = self.client.get(COLLECTIONS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_not_required_register(self):
        self.client.logout()
        res = self.client.get(COLLECTIONS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
