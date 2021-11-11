"""This module contains all the database table"""

from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models


# Create your models here.
class UserManager(BaseUserManager):
    """Our custom user model manager"""

    def create_user(self, email, password=None, **extra_fields):
        """Creat and save the new users"""
        if not email:
            raise ValueError("User must have and email address.")

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """Hleps you to create a super user will all the permissions"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom User Model that support email insted of username"""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"


class Tag(models.Model):
    """Tag model with its fields"""

    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)


class Ingredient(models.Model):
    """Ingredient model with its fields"""

    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)


class Recipe(models.Model):
    """Recipe model with its fields"""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    title = models.CharField(max_length=255)
    time_in_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.URLField(blank=True)
    tags = models.ManyToManyField(Tag)
    ingredients = models.ManyToManyField(Ingredient)

    def __str__(self):
        return str(self.title)
