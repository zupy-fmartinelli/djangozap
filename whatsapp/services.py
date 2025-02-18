import requests
from django.conf import settings


class EvolutionAPI:
    """Cliente para interagir com a Evolution API."""

    BASE_URL = settings.EVOLUTION_API_BASE_URL
    API_KEY = settings.EVOLUTION_API_KEY
    DEFAULT_INSTANCE = getattr(settings, "EVOLUTION_INSTANCE_NAME", None)

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
