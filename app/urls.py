from django.urls import path
from . import views

urlpatterns = [
    # Paths for pilot:
    path('', views.index, name='index'),
]