from rest_framework import serializers

from .models import Video


class VideoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Video
        fields = ('id', 'title', 'description', 'video_file', 'poster_image')

    def create(self, validated_data):
        validated_data.get('video_file').name = Video.hashing_file_name(validated_data.get('video_file').name)
        validated_data.get('poster_image').name = Video.hashing_file_name(validated_data.get('poster_image').name)
        video = Video.objects.create(**validated_data)
        video.save()
        return video

    def update(self, instance, validated_data):
        video_file = validated_data.pop('video_file', None)
        if video_file:
            instance.video_file.delete()
            video_file.name = Video.hashing_file_name(video_file.name)
            instance.video_file = video_file

        poster_image = validated_data.pop('poster_image', None)
        if poster_image:
            instance.poster_image.delete()
            poster_image.name = Video.hashing_file_name(poster_image.name)
            instance.poster_image = poster_image

        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)

        instance.save()
        return instance
