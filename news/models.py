from django.db import models

class News(models.Model):
    headline = models.CharField(max_length=200)
    body = models.TextField()
    date = models.DateTimeField()
    image = models.ImageField(upload_to="news/images/", default="news/images/default.jpg")
    
    def __str__(self):
        return self.headline