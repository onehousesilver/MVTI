from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    nickname = models.CharField(max_length=50)
    mbti = models.CharField(max_length=4, null=True)


class Profile():
    pass