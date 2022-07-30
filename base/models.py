from uuid import uuid4
from django.db import models
from django.contrib.auth.models import User

class Menu(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, null=False, blank=False, editable=False)
    owner = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    price = models.FloatField()
    image = models.CharField(unique=True, max_length=300)

    
    def __str__(self):
        return self.title 