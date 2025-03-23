from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    id = models.AutoField(primary_key=True)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    
    ROLES = [
        ('turista', 'Turista'),
        ('administrador', 'Administrador'),
        ('empleado', 'Empleado'),
    ]
    
    rol = models.CharField(max_length=20, choices=ROLES, default='turista')
    
    REQUIRED_FIELDS = ["email", "last_name"]