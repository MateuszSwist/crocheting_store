from uuid import uuid4
from django.contrib.auth.models import(
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
    )
from django.contrib.auth.hashers import make_password
from django.db import models

class StoreUserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('You must provide an email address')
        user=self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.is_email_confirmed = True
        user.save()
        return user

class StoreUser(AbstractBaseUser, PermissionsMixin):

    created = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_email_confirmed = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    objects = StoreUserManager()

    def __str__(self):
        return self.email

class EmailConfirmationToken(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False )
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(StoreUser, on_delete=models.CASCADE)
