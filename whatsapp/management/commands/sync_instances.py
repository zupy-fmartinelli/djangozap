import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from whatsapp.models import WhatsAppInstance

User = get_user_model()

# Definição de constantes para os status HTTP
HTTP_OK = 200
HTTP_UNAUTHORIZED = 401
HTTP_NOT_FOUND = 404


class Command(BaseCommand):
    help = "Sincroniza instâncias do WhatsApp da Evolution API para o Django"

    def handle(self, *args, **kwargs):
        url = f"{settings.EVOLUTION_API_BASE_URL}/instance/fetchInstances"
        headers = {
            "apikey": settings.EVOLUTION_API_KEY,
            "Accept": "application/json",
        }

        response = requests.get(
            url,
            headers=headers,
            timeout=10,
        )  # 🔥 Adicionamos timeout

        if response.status_code == HTTP_OK:
            data = response.json()
            instances = data

            default_user = User.objects.filter(is_superuser=True).first()
            if not default_user:
                self.stderr.write(
                    self.style.ERROR(
                        "Nenhum usuário encontrado para associar as instâncias!",
                    ),
                )
                return

            for instance in instances:
                WhatsAppInstance.objects.update_or_create(
                    instance_name=instance["name"],
                    phone_number=instance.get("ownerJid", "").replace(
                        "@s.whatsapp.net",
                        "",
                    ),
                    defaults={
                        "user": default_user,
                        "api_key": settings.EVOLUTION_API_KEY,
                        "is_active": instance["connectionStatus"] == "open",
                    },
                )

            self.stdout.write(
                self.style.SUCCESS(
                    f"✔ {len(instances)} instâncias sincronizadas com sucesso!",
                ),
            )

        else:
            self.stderr.write(
                self.style.ERROR(f"Erro ao buscar instâncias: {response.text}"),
            )
