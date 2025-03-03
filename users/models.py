# users/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    role = models.CharField(max_length=20, choices=[
        ('admin', 'Admin'),
        ('user', 'User'),
    ], default='user')

    def __str__(self):
        return self.username
