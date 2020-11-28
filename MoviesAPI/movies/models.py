from django.contrib.auth.models import User
from django.db import models


# Model to save the collections created.
class Collection(models.Model):
    title = models.CharField(max_length=30, default=None)
    description = models.TextField(default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


# Model to save the unique movies based on uuid
class Movie(models.Model):
    title = models.CharField(max_length=30, default=None)
    description = models.TextField(default=None)
    genres = models.TextField(default=None, null=True, blank=True)
    uuid = models.CharField(max_length=30, default=None, unique=True)

    def __str__(self):
        return self.title


# Model to map the collection and movies in it
class Relation(models.Model):
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
