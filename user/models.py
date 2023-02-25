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
    friend_requests_sent = models.ManyToManyField('self', related_name='user_friend_requests_sent', symmetrical=False,
                                                  blank=True)
    friend_requests_received = models.ManyToManyField('self', related_name='user_friend_requests_received',
                                                      symmetrical=False, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        """functional create random 6 digits and save to field "verification_code" for invite user"""
        if not self.pk:
            self.verification_code = random.randint(100000, 999999)
        super().save(*args, **kwargs)

    def send_friend_request(self, friend):
        if friend != self and not self.friend.filter(pk=friend.pk).exists() and not self.friend_requests_sent.filter(
                pk=friend.pk).exists() and not self.friend_requests_received.filter(pk=friend.pk).exists():
            self.friend_requests_sent.add(friend)
            friend.friend_requests_received.add(self)

    def accept_friend_request(self, friend):
        if friend in self.friend_requests_received.all():
            self.friend_requests_received.remove(friend)
            self.friend.add(friend)
            friend.friend.add(self)

    def reject_friend_request(self, friend):
        if friend in self.friend_requests_received.all():
            self.friend_requests_received.remove(friend)
            friend.friend_requests_sent.remove(self)

    def unfriend(self, friend):
        if friend in self.friend.all():
            self.friend.remove(friend)
            friend.friend.remove(self)
