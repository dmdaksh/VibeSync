from django.urls import path
from . import views

urlpatterns = [
    # Paths for pilot:
    path('', views.index, name='index'),
    path('get_yt_link/<str:search_query>/', views.get_youtube_link, name='get_yt_link'),
    path('get_yt_audio/<str:yt_id>/', views.get_yt_audio, name='get_yt_audio')
]