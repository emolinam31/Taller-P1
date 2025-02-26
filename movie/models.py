import django.db.models
from django.db import models

# Create your models here.

class Movie(django.db.models.Model):
    title = django.db.models.CharField(max_length=100)
    description = django.db.models.CharField(max_length=250)
    image = django.db.models.ImageField(upload_to="movie/images/")
    url = django.db.models.URLField(blank=True)
    genre = models.CharField(blank=True, max_length=100)
    year = models.IntegerField(blank=True, null=True)

    def __str__(self): return self.title
    
    