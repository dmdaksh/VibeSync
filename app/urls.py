from django.urls import path
from . import views

urlpatterns = [
    # Paths for pilot:
    path('', views.upload_video, name='upload_video'),
]