from django.urls import path
from . import views

urlpatterns = [
    # Paths for pilot:
    path('', views.index, name='index'),
    path('get_yt_link/<str:search_query>/', views.get_youtube_link, name='get_yt_link')
]