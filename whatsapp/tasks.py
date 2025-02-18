import logging

import phonenumbers
from celery import shared_task

from djangozap.users.models import User
from whatsapp.services import EvolutionAPI

logger = logging.getLogger(__name__)


def format_phone(phone):
    """Formata um número de telefone para o padrão internacional."""
    try:
        parsed = phonenumbers.parse(str(phone), "BR")
        return phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
    except phonenumbers.NumberParseException:
        logger.exception("Erro ao formatar telefone %s", phone)
        return None


@shared_task
def update_whatsapp_info(user_id):
    """Tarefa para buscar e atualizar informações do WhatsApp."""
    try:
        user = User.objects.get(id=user_id)

        if not user.phone_number:
            return f"⚠️ Usuário {user.email} sem número de telefone."

        phone_number = format_phone(user.phone_number)
        if not phone_number:
            return f"❌ Telefone inválido: {user.phone_number}"

        logger.info("🔍 Buscando WhatsApp para %s (%s)", user.email, phone_number)

        response = EvolutionAPI.check_is_whatsapp(user, [phone_number])

        if response and isinstance(response, list) and response[0].get("exists"):
            user.whatsapp_jid = response[0]["jid"]
            user.whatsapp_name = response[0].get("name", "")

            profile_pic = EvolutionAPI.fetch_profile_pic(user, phone_number)
            user.whatsapp_profile_pic = profile_pic
            user.save()

            logger.info(
                "✅ Atualizado %s | Nome: %s | Foto: %s",
                user.email,
                user.whatsapp_name,
                profile_pic,
            )
            return (
                f"✅ Atualizado {user.email} | Nome: {user.whatsapp_name} | "
                f"Foto: {profile_pic}"
            )

        logger.warning("❌ %s não tem WhatsApp válido.", user.email)
        return f"❌ {user.email} não tem WhatsApp válido."  # noqa: TRY300

    except User.DoesNotExist:
        logger.exception("❌ Usuário %s não encontrado.", user_id)
        return f"❌ Usuário {user_id} não encontrado."

    except Exception:
        logger.exception(
            "⚠️ Erro inesperado ao atualizar WhatsApp do usuário %s",
            user_id,
        )  # 🔥 `logger.exception` já inclui a exceção automaticamente!
        return f"⚠️ Erro inesperado ao atualizar WhatsApp do usuário {user_id}."
