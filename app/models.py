from django.db import models

# Create your models here.

class Video(models.Model):
    id = models.AutoField(primary_key=True)
    url = models.URLField(max_length=200)
