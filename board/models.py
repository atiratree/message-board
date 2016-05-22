import datetime

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Message(models.Model):
    author = models.ForeignKey(User)
    date = models.DateTimeField()
    title = models.CharField(max_length=70)
    content = models.CharField(max_length=500) 
    def __str__(self):
        return self.title + " : " + self.author.username
