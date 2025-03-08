# chatbot/models.py

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class ChatMessage(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    message = models.TextField()
    sender = models.CharField(max_length=10, choices=[
        ('user', 'User'),
        ('bot', 'Bot')
    ])
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, choices=[
        ('business_owner', 'Business Owner/Manager'),
        ('employee', 'Employee (General)'),
        ('it_staff', 'IT/Technical Staff')
    ])
    industry = models.CharField(max_length=100)
    company_size = models.CharField(max_length=20, choices=[
        ('small', 'Small (1-50)'),
        ('medium', 'Medium (51-200)'),
        ('large', 'Large (201+)')
    ])
    security_level = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])

    def __str__(self):
        return f"{self.user.username} - {self.role}"

class UserProgress(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    current_module = models.CharField(max_length=255, default="Introduction")
    progress_percentage = models.FloatField(default=0.0)
    completed_modules = models.JSONField(default=list)
    last_accessed = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.current_module} ({self.progress_percentage}%)"

class SecurityAssessment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    assessment_date = models.DateTimeField(auto_now_add=True)
    score = models.FloatField()
    recommendations = models.JSONField()
    risk_level = models.CharField(max_length=20, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    ])

    def __str__(self):
        return f"{self.user.username} - Assessment on {self.assessment_date}"

class SecurityScenario(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    difficulty = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    industry = models.CharField(max_length=100)
    role = models.CharField(max_length=50, choices=[
        ('owner', 'Owner'),
        ('manager', 'Manager'),
        ('employee', 'Employee')
    ])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title