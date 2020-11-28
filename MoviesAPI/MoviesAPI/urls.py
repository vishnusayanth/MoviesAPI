from django.urls import path, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter

from movies import views as movie_views
from user import views as user_views
from app import views as app_views

router = DefaultRouter()
router.register('', movie_views.CollectionView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('movies/', movie_views.movies, name='movies'),
    path('collection/', include(router.urls), name='collection'),
    path('register/', user_views.RegisterView.as_view(), name='register'),
    path('request-count/', app_views.request_count, name='request_count'),
    path('request-count/reset/', app_views.reset_request_count, name='reset_request_count')
]
