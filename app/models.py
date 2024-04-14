from django.db import models

# Create your models here.

class Video(models.Model):
    id = models.AutoField(primary_key=True)
    url = models.URLField(max_length=200)

class YouTubeVideo(models.Model):
    video_link = models.URLField()
    search_query = models.CharField(max_length=255)