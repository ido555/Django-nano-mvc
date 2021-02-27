from uuid import uuid4

from django.db import models

# Create your models here.
from django.db import models


# class Question(models.Model):
# question_text = models.CharField(max_length=65535)
# pub_date = models.DateTimeField('date published')

# TODO implement symmetric encryption on the JWT token and only
#  send the encrypted JWT to the client (with fernet) (if i have enough time)
class User(models.Model):
    username = models.CharField(max_length=255, default="")
    password = models.CharField(max_length=255, default="")
