import json

import requests
from django.conf import settings
from django.contrib import admin
from django.contrib import messages

from .models import WhatsAppInstance


@admin.register(WhatsAppInstance)
class WhatsAppInstanceAdmin(admin.ModelAdmin):
    """Admin para gerenciar instâncias do WhatsApp."""

    list_display = (
        "instance_name",
        "phone_number",
        "integration_type",
        "is_active",
        "created_at",
        "qrcode_display",
    )
    search_fields = ("instance_name", "phone_number")
    list_filter = ("is_active", "integration_type")
    actions = ["create_instance"]

    @admin.action(description="Criar Instância no Evolution API")
    def create_instance(self, request, queryset):
        """Ação para criar instância na Evolution API."""
        for obj in queryset:
            self.save_whatsapp_instance(
                request,
                obj,
                self.get_form(request, obj, change=False),
            )

    @admin.display(description="QR Code")
    def qrcode_display(self, obj):
        """Exibe a imagem do QR Code no Admin."""

    def save_whatsapp_instance(self, request, obj, form, *, change=False):
        """Cria a instância na Evolution API e armazena os dados."""
        # Usando a URL da Evolution API do settings
        api_url = f"{settings.evolution_api_base_url}/instance/create"
        headers = {
            "apikey": settings.evolution_api_key,
            "Content-Type": "application/json",
        }
        payload = {
            "instanceName": obj.instance_name,
            "token": "",
            "qrcode": True,
            "number": obj.phone_number,
            "integration": obj.integration_type,
            "webhook": "",
            "webhook_by_events": True,
            "events": ["APPLICATION_STARTUP"],
            "reject_call": True,
            "msg_call": "Não aceitamos chamadas!",
            "groups_ignore": True,
            "always_online": True,
            "read_messages": True,
            "read_status": True,
            "websocket_enabled": False,
            "rabbitmq_enabled": False,
            "sqs_enabled": False,
        }

        try:
            response = requests.post(
                api_url,
                json=payload,
                headers=headers,
                timeout=10,
            )  # Fix for S113
            if response.status_code in [200, 201]:  # Aceita tanto 200 quanto 201
                data = response.json()
                if "error" in data:  # Fix for TRY300
                    messages.error(request, f"⚠ Erro na API: {data['error']}")
                else:
                    obj.instance_id = data["instance"]["instanceId"]
                    obj.is_active = data["instance"]["status"] == "connecting"
                    obj.qrcode_url = data.get("qrcode", {}).get("base64", "")

                    super().save_model(request, obj, form, change)
                    messages.success(request, "✅ Instância criada com sucesso!")
            else:
                messages.error(
                    request,
                    f"❌ Erro ao criar a instância! Código {response.status_code}",
                )
        except (requests.RequestException, KeyError, json.JSONDecodeError) as e:
            messages.error(request, f"⚠ Erro ao processar resposta da API: {e!s}")
