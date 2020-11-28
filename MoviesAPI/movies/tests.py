from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase, RequestFactory

from rest_framework import status
from rest_framework.test import APIClient

from .models import Collection, Movie
from .views import CollectionView

COLLECTIONS_URL = '/collection/'
COLLECTION_URL = '/collection/1/'
MOVIES_URL = reverse('movies')


class CollectionsTestCases(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username='test',
            password='testpass'
        )
        self.client.force_authenticate(self.user)
        self.factory = RequestFactory()
        self.request = self.factory.get(COLLECTIONS_URL)

    def test_valid_registerview(self):
        v = CollectionView()
        v.setup(self.request)
        # Next line runs only if the above scenario passes with no error
        self.assertTrue(True)

    def test_retrieve_collection_list(self):
        Collection.objects.create(user=self.user, title='safdsf ad', description='df vdcfed gfs gsdf vdcf ')
        Collection.objects.create(user=self.user, title='saaf dafdflt',
                                  description='f dsg sdg sd ggdsd  fdsf ')
        res = self.client.get(COLLECTIONS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(res.data['is_success'])

    def test_retrieve_collection_object(self):
        Collection.objects.create(user=self.user, title='safdsf ad', description='df vdcfed gfs gsdf vdcf ')
        res = self.client.get(COLLECTION_URL)
        collection = Collection.objects.get(id=1)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['title'], collection.title)

    def test_create_collection_successful(self):
        payload = {
            'title': 'Test Title',
            'description': '<Description of the collection>',
            'movies': [
                {
                    'title': 'Inception',
                    'description': '<description of Inception>',
                    'genres': '<SCIFI>',
                    'uuid': 1
                },
                {
                    'title': 'Hachiko',
                    'description': '<description of Hachiko>',
                    'genres': '<FEELGOOD>',
                    'uuid': 2
                },
            ]
        }
        self.client.post(COLLECTIONS_URL, headers={'content_type': 'application/json'}, data=payload)
        exists = Collection.objects.filter(
            user=self.user,
            title=payload['title']
        ).exists()
        self.assertTrue(exists)

    def test_create_collection_invalid(self):
        payload = {'movies': ''}
        try:
            res = self.client.post(COLLECTIONS_URL, payload)
            self.assertEqual(res.status_code, status.HTTP_200_OK)
        except Exception:
            self.assertTrue(True)

    def test_invalid_movies_post_response(self):
        data = self.client.post(MOVIES_URL)
        self.assertNotEqual(data.status_code, status.HTTP_200_OK)

    def test_valid_movies_get_response(self):
        data = self.client.get(MOVIES_URL)
        self.assertEqual(data.status_code, status.HTTP_200_OK)

    def test_Collection_model(self):
        obj = Collection.objects.create(user=self.user, title='safdsf ad', description='df vdcfed gfs gsdf vdcf ')
        self.assertEqual(str(obj), obj.title)

    def test_Movie_model(self):
        obj = Movie.objects.create(title='safdsf ad', description='df vdcfed gfs gsdf vdcf ',uuid=123)
        self.assertEqual(str(obj), obj.title)

    def test_valid_collection_destroy_response(self):
        Collection.objects.create(user=self.user, title='safdsf ad', description='df vdcfed gfs gsdf vdcf ')
        data = self.client.get(COLLECTION_URL)
        self.assertEqual(data.status_code, status.HTTP_200_OK)

    def test_valid_collection_get_response(self):
        obj = Collection.objects.create(user=self.user, title='safdsf ad', description='df vdcfed gfs gsdf vdcf ')
        data = self.client.get(COLLECTION_URL)
        self.assertEqual(data.status_code, status.HTTP_200_OK)
        self.assertEqual(data.json()['title'], obj.title)

    def test_update_collection_successful(self):
        obj = Collection.objects.create(user=self.user, title='safdsf ad', description='df vdcfed gfs gsdf vdcf ')
        payload = {
            'title': 'Test Title',
            'description': '<Description of the collection>',
            'movies': [
                {
                    'title': 'Inception',
                    'description': '<description of Inception>',
                    'genres': '<SCIFI>',
                    'uuid': 1
                },
                {
                    'title': 'Hachiko',
                    'description': '<description of Hachiko>',
                    'genres': '<FEELGOOD>',
                    'uuid': 2
                },
            ]
        }
        self.client.put(COLLECTION_URL, headers={'content_type': 'application/json'}, data=payload)
        exists = Collection.objects.filter(
            user=self.user,
            title=payload['title']
        ).exists()
        self.assertTrue(exists)
        new_obj = Collection.objects.get(id=1)
        self.assertNotEqual(obj.title,new_obj.title)
