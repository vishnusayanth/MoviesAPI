from django.contrib import admin

from movies.models import Collection, Movie, Relation

# Models registered to admin if the default admin panel is to be used in the future,
admin.site.register(Collection)
admin.site.register(Movie)
admin.site.register(Relation)
