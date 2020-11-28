from django.contrib import admin

from app.models import RequestCounter

# Models registered to admin if the default admin panel is to be used in the future,
admin.site.register(RequestCounter)
