import uuid

from django.contrib.auth import get_user_model
from django.db import models
from storages.backends.s3boto3 import S3Boto3Storage


class Video(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    video_file = models.FileField(storage=S3Boto3Storage(), upload_to='videos/', unique=True)
    poster_image = models.ImageField(storage=S3Boto3Storage(), upload_to='posters/', unique=True)

    def __str__(self):
        return self.title

    @staticmethod
    def hashing_file_name(name):
        extension = name.split('.')[-1]
        return f'{uuid.uuid4().hex}.{extension}'


class Room(models.Model):
    owner = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
