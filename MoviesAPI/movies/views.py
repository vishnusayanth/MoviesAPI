import requests
from django.http import JsonResponse, HttpResponse
from requests.auth import HTTPBasicAuth
from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from app import utils
from app.utils import get_favourite_genres
from movies.models import Collection, Movie, Relation
from movies.serializers import CollectionSerializer


def movies(request):
    if request.method == 'POST':
        return HttpResponse(status=500)
    user_pass = HTTPBasicAuth(utils.API_USERNAME, utils.API_PASSWORD)
    result = requests.get(utils.MOVIE_URL, auth=user_pass)
    # return the result from the api for movies as a Json Response
    return JsonResponse(result.json())


class CollectionView(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin, mixins.RetrieveModelMixin, ):
    queryset = Collection.objects.all()
    permission_classes = IsAuthenticated,
    serializer_class = CollectionSerializer
    authentication_classes = TokenAuthentication,

    def list(self, request, *args, **kwargs):
        items = self.queryset.filter(user=self.request.user)
        collection = self.get_serializer(items, many=True).data
        data = {
            "data": {
                "collections": collection,
                'favourite_genres': get_favourite_genres(self.request.user),
                # favourite genres are fetched from a custom function that returns a list of favourite genres.
            },
            'is_success': True,
        }
        # list function is overridden to create a custom response
        return Response(data=data, status=status.HTTP_200_OK, content_type='application/json')

    def perform_create(self, serializer):
        movies_dict = self.request.data['movies']
        collection = serializer.save(user=self.request.user)
        # serializer is saved by setting the current user as the user.
        # For each movie in the request,
        # if the movie's uuid does not exist in database, new movie is created
        # a relation object is created mapping the movie and the collection.
        for item in movies_dict:
            if not Movie.objects.filter(uuid=item['uuid']).exists():
                movie = Movie(uuid=item['uuid'], description=item['description'], title=item['title'],
                              genres=item['genres'])
                movie.save()
            else:
                movie = Movie.objects.get(uuid=item['uuid'])
            relation = Relation(collection_id=collection.id, movie_id=movie.id)
            relation.save()
        # This function by default returns the serializer's attributes which contains the unique id.

    def retrieve(self, request, *args, **kwargs):
        # object is retrieved from database using primary key from kwargs.
        collection = Collection.objects.get(id=kwargs['pk'])
        response = {
            'title': collection.title,
            'description': collection.description,
            'number of movies in collection': len(
                Movie.objects.filter(relation__in=Relation.objects.filter(collection__user=request.user)))
            # Movies are filtered based on the collections created by the logged in user.
        }
        # Dictionary is returned in form of Response with status code 200
        return Response(data=response, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        event = Collection.objects.get(id=kwargs['pk'])
        event.delete()
        # Relation objects will be deleted by default because of models.CASCADE.
        # Movie objects with uuid will remain for future use.
        return JsonResponse(
            {
                'status': status.HTTP_200_OK,
                'message': 'Deleted the collection successfully!'
            }
        )

    def update(self, request, *args, **kwargs):
        collection = Collection.objects.get(id=kwargs['pk'])
        collection.title = request.data['title']
        collection.description = request.data['description']
        collection.save()
        Relation.objects.filter(collection_id=collection.id).delete()
        # Collection object is updated first and the Relation objects are deleted.
        # The Relation objects are created based on existing movies in db or new movies if any
        movies_dict = self.request.data['movies']
        for item in movies_dict:
            if not Movie.objects.filter(uuid=item['uuid']).exists():
                movie = Movie(uuid=item['uuid'], description=item['description'], title=item['title'],
                              genres=item['genres'])
                movie.save()
            else:
                movie = Movie.objects.get(uuid=item['uuid'])
            relation = Relation(collection_id=collection.id, movie_id=movie.id)
            relation.save()
        # collection unique id and a success message is returned.
        return JsonResponse({
            'id': collection.id,
            'message': 'Updated the collection successfully!'
        })
