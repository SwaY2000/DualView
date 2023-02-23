from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import User
from .utils import pattern_password


class InviteUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=20, validators=[UniqueValidator(queryset=User.objects.all())])
    email = serializers.EmailField(max_length=255, validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(validators=[pattern_password])

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        return User.objects.create(**validated_data)
