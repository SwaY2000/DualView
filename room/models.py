from django.db import models
from storages.backends.s3boto3 import S3Boto3Storage


class Video(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    video_file = models.FileField(storage=S3Boto3Storage(), upload_to='videos/')
    poster_image = models.ImageField(storage=S3Boto3Storage(), upload_to='posters/')

    def __str__(self):
        return self.title
