# Create your models here.
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class WhatsAppInstance(models.Model):
    """Representa uma instância da Evolution API vinculada a uma empresa."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="whatsapp_instances",
    )
    instance_name = models.CharField(max_length=255, unique=True)
    api_key = models.CharField(
        max_length=255,
        help_text="Chave de API para autenticação",
    )
    phone_number = models.CharField(
        max_length=20,
        help_text="Número de telefone vinculado",
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.instance_name} ({self.phone_number})"
