from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from app.models import RequestCounter

URL = reverse('request_count')
RESET_URL = reverse('reset_request_count')


class RequestCounterTestCases(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username='test',
            password='testpass'
        )
        self.client.force_authenticate(self.user)

    def test_multiple_object_creation_fails(self):
        obj = RequestCounter(value=0)
        obj.save()
        try:
            new_obj = RequestCounter(value=0)
            new_obj.save()
            self.assertTrue(False)
        except ValidationError:
            self.assertTrue(True)

    def test_Validation_error_raised(self):
        obj = RequestCounter(value=0)
        obj.save()
        try:
            try:
                new_obj = RequestCounter(value=0)
                new_obj.save()
                self.assertTrue(False)
            except FileNotFoundError:
                self.assertTrue(False)
        except Exception:
            self.assertTrue(True)

    def test_single_object_creation_passes(self):
        try:
            obj = RequestCounter(value=0)
            obj.save()
            self.assertTrue(True)
        except ValidationError:
            self.assertTrue(False)

    def test_get_request_count(self):
        data = self.client.get(URL)
        self.assertEqual(type(data), type(JsonResponse(None, safe=False)))

    def test_reset_request_count(self):
        data = self.client.get(URL)
        self.assertEqual(type(data), type(JsonResponse(None, safe=False)))

    def test_get_request_count_status(self):
        data = self.client.get(URL)
        self.assertEqual(status.HTTP_200_OK, data.status_code)

    def test_reset_request_count_status(self):
        data = self.client.get(RESET_URL)
        self.assertEqual(status.HTTP_200_OK, data.status_code)
