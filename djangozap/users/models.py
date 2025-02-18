from typing import ClassVar

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from .managers import UserManager


class User(AbstractUser):
    """Modelo de usuário customizado para o DjangoZap.

    Se adicionar campos necessários no cadastro, verifique os formulários
    SignupForm e SocialSignupForm.
    """

    # Primeiro e último nome removidos (não são úteis para todos os casos)
    name = models.CharField(_("Nome do Usuário"), blank=True, max_length=255)
    first_name = None  # type: ignore[assignment]
    last_name = None  # type: ignore[assignment]
    email = models.EmailField(_("Email"), unique=True)
    username = None  # type: ignore[assignment]

    # Dados do WhatsApp
    phone_number = PhoneNumberField(
        _("Número de Telefone"),
        region="BR",
        blank=True,
        null=True,
        unique=True,
    )
    whatsapp_jid = models.CharField(
        _("JID do WhatsApp"),
        max_length=50,
        blank=True,
    )
    whatsapp_name = models.CharField(
        _("Nome no WhatsApp"),
        max_length=255,
        blank=True,
    )
    whatsapp_profile_pic = models.URLField(
        _("Foto de Perfil do WhatsApp"),
        blank=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects: ClassVar[UserManager] = UserManager()

    def get_absolute_url(self) -> str:
        """Retorna a URL do detalhe do usuário."""
        return reverse("users:detail", kwargs={"pk": self.id})

    def __str__(self):
        """Retorna uma string representativa do usuário."""
        return self.name if self.name else self.email
