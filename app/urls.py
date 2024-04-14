from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    # Paths for pilot:
    path('', views.index, name='index'),
    path('get_yt_link/', views.get_youtube_link, name='get_yt_link'),
    # path('get_yt_audio/<str:yt_id>/', views.get_yt_audio, name='get_yt_audio')
    path('get_status/', views.get_status, name='get_status'),
]