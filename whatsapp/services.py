import requests
from django.conf import settings

# Definição de constantes para os status HTTP
HTTP_OK = 200
HTTP_UNAUTHORIZED = 401
HTTP_NOT_FOUND = 404


class EvolutionAPI:
    """Cliente para interagir com a Evolution API"""

    BASE_URL = settings.EVOLUTION_API_BASE_URL
    API_KEY = settings.EVOLUTION_API_KEY

    @classmethod
    def get_instances(cls):
        """Busca todas as instâncias já criadas na Evolution API"""
        url = f"{cls.BASE_URL}/instance/fetchInstances"
        headers = {
            "apikey": cls.API_KEY,
            "Accept": "application/json",
        }

        response = requests.get(
            url,
            headers=headers,
            timeout=10,
        )  # 🔥 Adicionamos timeout

        if response.status_code == HTTP_OK:
            return response.json()
        if response.status_code == HTTP_UNAUTHORIZED:
            return {"error": "🔴 ERRO 401: API Key inválida ou não autorizada!"}
        if response.status_code == HTTP_NOT_FOUND:
            return {"error": "🔴 ERRO 404: Endpoint não encontrado! Verifique a URL."}

        return {"error": f"Erro ao buscar instâncias: {response.text}"}
