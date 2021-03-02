from django.db.models import QuerySet
from django.test import TestCase
from .models import User
from django.core.exceptions import ValidationError


class UserModelTests(TestCase):
    def test_usernameTooLong(self):
        user = User(username="a"*400)
        # print(user.username)
        # user.save()
        # dbUsername = QuerySet(model=User).last().username
        self.assertRaises(ValidationError, user.full_clean(), True)
