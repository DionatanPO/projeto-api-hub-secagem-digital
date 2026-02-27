from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('EQUIPE', 'Equipe'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='EQUIPE')

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
