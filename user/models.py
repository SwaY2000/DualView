import random

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=20, unique=True)
    email = models.EmailField(db_index=True, unique=True)
    verification_code = models.IntegerField(null=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    friend = models.ManyToManyField('self', related_name='friends', symmetrical=False, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        '''functional create random 6 digits and save to field "verification_code" for invite user'''
        if not self.pk:
            self.verification_code = random.randint(100000, 999999)
        super().save(*args, **kwargs)
