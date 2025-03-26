from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Role(models.Model):
    role_id = models.AutoField(primary_key=True, verbose_name="Id")
    role = models.CharField(max_length=30, verbose_name="Role")

    def __str__(self):
        return self.role

class User(AbstractUser):
    user_id = models.AutoField(primary_key=True, verbose_name="Id")
    name = models.CharField(max_length=50, verbose_name="Name")
    last_name = models.CharField(max_length=50, verbose_name="Last Name")
    username = models.CharField(max_length=50, unique=True, verbose_name="Username")
    email = models.EmailField(unique=True, verbose_name="Email")
    role_id = models.ForeignKey(Role, on_delete=models.CASCADE, verbose_name='Rol', null=True, blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'name', 'last_name']

    def __str__(self):
        return self.username