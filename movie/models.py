import django.db.models
from django.db import models
import numpy as np



def get_defauly_array():
    default_arr = np.random.rand(1536)
    return default_arr.tobytes()

class Movie(django.db.models.Model):
    title = django.db.models.CharField(max_length=100)
    description = django.db.models.TextField(max_length=5000)
    image = django.db.models.ImageField(upload_to="movie/images/", default="movie/images/default.jpg")
    url = django.db.models.URLField(blank=True)
    genre = models.CharField(blank=True, max_length=100)
    year = models.IntegerField(blank=True, null=True)
    emb = models.BinaryField(default=get_defauly_array())

    def __str__(self): 
        return self.title
    
    