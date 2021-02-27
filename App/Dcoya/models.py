from uuid import uuid4

from django.db import models

# Create your models here.
from django.db import models


# class Question(models.Model):
# question_text = models.CharField(max_length=65535)
# pub_date = models.DateTimeField('date published')

# TODO implement a date of creation for the token's expiry date
#  + a way to update the expiry date for each action from the user
#   if theres enough time
class User(models.Model):
    username = models.CharField(max_length=255, default="")
    password = models.CharField(max_length=255, default="")
    token = models.CharField(max_length=1024, default="")
