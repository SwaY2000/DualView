from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import User
from .utils import pattern_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'friend', 'friend_requests_sent', 'friend_requests_received']


class InviteUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=20, validators=[UniqueValidator(queryset=User.objects.all())])
    email = serializers.EmailField(max_length=255, validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(validators=[pattern_password])

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class ActivateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['verification_code']

    def validate(self, data):
        if getattr(self, 'instance', None).verification_code != data.get('verification_code'):
            raise serializers.ValidationError('Wrong verification_code')
        return data

    def update(self, instance, validated_data):
        instance.is_active = True
        instance.verification_code = None
        instance.save()
        return instance
