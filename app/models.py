from django.db import models

# Create your models here.

class Video(models.Model):
    id = models.AutoField(primary_key=True)

class YouTubeVideo(models.Model):
    video_link = models.URLField()
    search_query = models.CharField(max_length=255)