from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
# router.register(r'movies', views.MovieView, base_name='movie')

# router.register('movies', views.moviesList)

urlpatterns = [
    path('', include(router.urls)),
    path(r'movies',views.MovieView),
    path(r'comments',views.CommentView),
    path(r'top',views.TopView)
]