from uuid import uuid4
from django.db import models
from django.contrib.auth.models import User

class Menu(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, null=False, blank=False, editable=False)
    owner = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    price = models.FloatField()
    image = models.CharField(unique=True, max_length=300)
    token = models.CharField(max_length=200)
    
    def __str__(self):
        return self.title 

class News(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, null=False, blank=False, editable=False)
    body = models.CharField(max_length=200)
    broadcaster = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[0:50]

    class Meta:
        ordering = ('-date',)