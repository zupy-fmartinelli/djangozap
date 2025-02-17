import requests
from django.conf import settings

# Definição de constantes para os status HTTP
HTTP_OK = 200
HTTP_UNAUTHORIZED = 401
HTTP_NOT_FOUND = 404
HTTP_CREATED = 201


class EvolutionAPI:
    """Cliente para interagir com a Evolution API"""

    BASE_URL = settings.EVOLUTION_API_BASE_URL
    API_KEY = settings.EVOLUTION_API_KEY

    @classmethod
    def create_instance(cls, instance_name, integration="WHATSAPP-BAILEYS"):
        """Cria uma nova instância no Evolution API e retorna o QR Code + API Key"""
        url = f"{cls.BASE_URL}/instance/create"
        headers = {
            "apikey": cls.API_KEY,
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        payload = {
            "instanceName": instance_name,
            "qrcode": True,  # 🔥 Pede para a API já gerar o QR Code
            "integration": integration,  # Pode ser BAILEYS, BUSINESS ou EVOLUTION
        }

        response = requests.post(url, headers=headers, json=payload, timeout=10)

        if response.status_code in [HTTP_OK, HTTP_CREATED]:
            data = response.json()
            return {
                "instance_id": data.get("id"),
                "api_key": data.get("token"),  # 🔥 API Key gerada automaticamente
                "qrcode_url": data.get("qrcode"),  # URL do QR Code
                "token": data.get("token"),
            }
        return {"error": f"Erro ao criar instância: {response.text}"}
