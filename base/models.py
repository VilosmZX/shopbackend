from django.db import models
from django.contrib.auth.models import User

class Menu(models.Model):
    owner = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    price = models.FloatField()
    image = models.ImageField(upload_to='media/menus')

    
    def __str__(self):
        return self.title 