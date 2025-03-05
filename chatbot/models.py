# chatbot/models.py

from django.db import models
from django.contrib.auth.models import User

class UserProgress(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_module = models.CharField(max_length=255, default="Introduction")
    progress_percentage = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.user.username} - {self.current_module} ({self.progress_percentage}%)"
