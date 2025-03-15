# users/models.py
# from django.contrib.auth.models import AbstractUser, Group, Permission
# from django.db import models

# class CustomUser(AbstractUser):
#     id = models.BigAutoField(primary_key=True)
    
#     groups = models.ManyToManyField(
#         Group,
#         related_name="customuser_groups",
#         blank=True
#     )
#     user_permissions = models.ManyToManyField(
#         Permission,
#         related_name="customuser_permissions",
#         blank=True
#     )

#     def __str__(self):
#         return self.username
    

# users/models.py
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils import timezone

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('business_owner', 'Business Owner/Manager'),
        ('employee', 'Employee'),
        ('technical_staff', 'IT/Technical Staff')
    ]
    
    id = models.BigAutoField(primary_key=True)
    groups = models.ManyToManyField(
        Group,
        related_name="customuser_groups",
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_permissions",
        blank=True
    )
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, null=True, blank=True)
    role_selected_at = models.DateTimeField(null=True, blank=True)
    first_login = models.BooleanField(default=True)  # Track first login status
    
    def __str__(self):
        return self.username