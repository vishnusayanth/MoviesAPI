from collections import Counter
import os
from app.models import RequestCounter
from movies.models import Relation

MOVIE_URL = 'https://demo.credy.in/api/v1/maya/movies/'

API_USERNAME = os.environ['API_USERNAME']
API_PASSWORD = os.environ['API_PASSWORD']


# Custom middleware to track the requests servered by this API
def counter_middleware(get_response):
    def middleware(request):
        item = RequestCounter.objects.first()
        if item is None:
            item = RequestCounter(value=0)
        item.value += 1
        item.save()
        response = get_response(request)
        return response

    return middleware


# Favourite genres of the user is found using this function
def get_favourite_genres(user):
    items = Relation.objects.filter(collection__user=user)
    counter_dict = dict()
    return_list = list()
    for item in items:
        if item.movie.genres is not None and item.movie.genres != '':
            # genres are stored as comma separated values in the movie attribute 'genres'.
            genres = item.movie.genres.split(',')
            # this is split into an array and looped through to find the count of individual genre
            for genre in genres:
                if genre not in counter_dict:
                    counter_dict[genre] = 0
                counter_dict[genre] += 1
            # for each genre, the count is incremented in the count dictionary
    k = Counter(counter_dict)
    most = k.most_common(3)
    # the most common 3 genres are found using the Counter function.
    for item in most:
        return_list.append(item[0])
    return return_list
