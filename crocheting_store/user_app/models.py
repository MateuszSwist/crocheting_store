from uuid import uuid4
from django.contrib.auth.models import(
    AbstractBaseUser,
    PermissionsMixin
    )
from django.contrib.auth.hashers import make_password
from django.db import models




class StoreUser(AbstractBaseUser):

    email = models.EmailField(unique=True)
    password = models.CharField(max_length=30)
    username = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created = models.DateField(auto_now_add=True)

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.username

class EmailConfirmationToken(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False )
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(StoreUser, on_delete=models.CASCADE)
