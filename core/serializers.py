from rest_framework import serializers
from .models import SystemCheckLog

class SystemCheckLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemCheckLog
        fields = '__all__'

    def validate(self, data):
        status = data.get('status')
        db_status = data.get('database_status', '').strip().lower()
        cache_status = data.get('cache_status', '').strip().lower()
        response_time = data.get('response_time_ms')

        if status not in ['ok', 'error']:
            raise serializers.ValidationError({"status": "Must be either 'ok' or 'error'."})

        if len(db_status) < 3:
            raise serializers.ValidationError({"database_status": "Must be at least 3 characters long."})

        if len(cache_status) < 3:
            raise serializers.ValidationError({"cache_status": "Must be at least 3 characters long."})

        if response_time is not None and response_time < 0:
            raise serializers.ValidationError({"response_time_ms": "Must be zero or positive."})

        if status == 'ok' and ('error' in db_status or 'error' in cache_status):
            raise serializers.ValidationError(
                "If status is 'ok', database_status and cache_status must not contain errors."
            )

        return data
