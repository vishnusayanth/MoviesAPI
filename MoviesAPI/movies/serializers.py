from rest_framework import serializers

from app.utils import get_favourite_genres
from .models import Collection


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ('id', 'title', 'description')
        read_only_fields = ('id',)

