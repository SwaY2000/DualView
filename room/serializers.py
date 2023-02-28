from rest_framework import serializers
from storages.backends.s3boto3 import S3Boto3Storage

from .models import Video


class VideoSerializer(serializers.ModelSerializer):
    video_file = serializers.FileField()

    class Meta:
        model = Video
        fields = ('id', 'title', 'description', 'video_file')

    def create(self, validated_data):
        video_file = validated_data.pop('video_file')
        video = Video.objects.create(video_file=video_file, **validated_data)

        storage = S3Boto3Storage()
        video_url = storage.url(video.video_file.name)
        video.video_url = video_url
        video.save()
        return video
