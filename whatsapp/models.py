from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class WhatsAppInstance(models.Model):
    """Representa uma instância da Evolution API vinculada a uma empresa."""

    INTEGRATION_CHOICES = [
        ("WHATSAPP-BAILEYS", "Baileys (Não Oficial)"),
        ("WHATSAPP-BUSINESS", "WhatsApp Cloud API (Oficial)"),
        ("EVOLUTION", "Evolution API"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="whatsapp_instances",
    )
    instance_name = models.CharField(max_length=255, unique=True)
    api_key = models.CharField(
        max_length=255,
        blank=True,
        default="",
        help_text="Chave de API gerada automaticamente",
    )
    phone_number = models.CharField(
        max_length=20,
        help_text="Número de telefone vinculado",
    )
    integration_type = models.CharField(
        max_length=20,
        choices=INTEGRATION_CHOICES,
        default="WHATSAPP-BAILEYS",
        help_text="Tipo de integração com WhatsApp",
    )
    token = models.CharField(
        max_length=255,
        blank=True,
        default="",
        help_text="Token da instância gerado pela API",
    )
    qrcode_url = models.URLField(
        blank=True,
        default="",
        help_text="URL do QR Code para ativação da instância",
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Método recomendado para representação do modelo no Django Admin."""
        return f"{self.instance_name} ({self.phone_number})"
