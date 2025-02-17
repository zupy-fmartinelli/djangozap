from rest_framework import serializers

from .models import WhatsAppInstance


class WhatsAppInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WhatsAppInstance
        fields = ["id", "instance_name", "phone_number", "is_active", "created_at"]
        read_only_fields = ["id", "created_at"]
