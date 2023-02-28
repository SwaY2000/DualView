import boto3
from django.db import models

class Video(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    video_file = models.S3Boto3StorageField(upload_to='videos/')
    poster_file = models.S3Boto3StorageField(upload_to='posters/', validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])])

    def __str__(self):
        return self.title