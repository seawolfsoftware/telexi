from .models import PressEvent
from rest_framework import serializers
from django.contrib.auth.models import User


class PressEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = PressEvent
        fields = ('id', 'device_id', 'is_button_on', 'created_at')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'password')
