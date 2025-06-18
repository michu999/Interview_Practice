from rest_framework import serializers
from .models import AIModelLog

class AIModelLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIModelLog
        fields = '__all__'
        read_only_fields = ('id', 'timestamp', 'processing_time')