from rest_framework import serializers
from .models import PressEvent


class PressEventSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'device_id', 'is_button_on', 'created_at')
        model = PressEvent
