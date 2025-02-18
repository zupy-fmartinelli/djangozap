import requests
from django.conf import settings

from whatsapp.models import WhatsAppInstance


class EvolutionAPI:
    """Cliente para interagir com a Evolution API."""

    BASE_URL = settings.EVOLUTION_API_BASE_URL
    API_KEY = settings.EVOLUTION_API_KEY
    DEFAULT_INSTANCE = getattr(settings, "EVOLUTION_INSTANCE_NAME", None)  # Fallback

    @classmethod
    def get_instance(cls, user):
        """Retorna a instância do usuário ou a padrão."""
        instance = WhatsAppInstance.objects.filter(user=user, is_active=True).first()
        return instance.instance_name if instance else cls.DEFAULT_INSTANCE

    @classmethod
    def send_message(cls, user, number, message):
        """Envia uma mensagem via WhatsApp usando a instância correta."""
        instance = cls.get_instance(user)  # 🔥 Busca a instância correta

        if not instance:
            return {"error": "Nenhuma instância disponível!"}

        url = f"{cls.BASE_URL}/message/sendText/{instance}"
        headers = {
            "apikey": cls.API_KEY,
            "Content-Type": "application/json",
        }
        payload = {
            "number": number,
            "text": message,
        }

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=10)
            return (
                response.json()
                if response.status_code in [200, 201]
                else {"error": response.text}
            )
        except requests.RequestException as e:
            return {"error": f"Erro na requisição: {e!s}"}

    @classmethod
    def check_is_whatsapp(cls, user, numbers):
        """Verifica se o número possui WhatsApp."""
        url = f"{cls.BASE_URL}/check"
        headers = {"apikey": cls.API_KEY}
        payload = {"numbers": numbers}

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=10)

            if response.status_code in [200, 201]:
                return response.json()
            return {  # noqa: TRY300
                "error": (
                    f"Erro ao verificar números: {response.status_code} - "
                    f"{response.text}"
                ),
            }
        except requests.RequestException as e:
            return {"error": f"Erro na requisição: {e!s}"}

    @classmethod
    def create_instance(cls, instance_name, integration_type, phone_number, user):
        """Cria uma nova instância no Evolution API e salva no banco de dados."""
        url = f"{cls.BASE_URL}/instance/create"
        headers = {
            "apikey": cls.API_KEY,
            "Content-Type": "application/json",
        }
        payload = {
            "instanceName": instance_name,
            "token": "",
            "qrcode": True,
            "number": phone_number,
            "integration": integration_type,
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
            response = requests.post(url, headers=headers, json=payload, timeout=15)
            data = response.json()

            if "error" in data:
                return {"error": data["error"]}
            return data  # noqa: TRY300

        except requests.RequestException as e:
            return {"error": f"Erro na requisição: {e!s}"}
