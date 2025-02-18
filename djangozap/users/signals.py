from django.db.models.signals import post_save
from django.dispatch import receiver

from djangozap.users.models import User
from whatsapp.services import EvolutionAPI


@receiver(post_save, sender=User)
def fetch_whatsapp_data(sender, instance, created, **kwargs):
    """Quando um usuário é criado, busca os dados do WhatsApp automaticamente."""
    if created and instance.phone_number:
        data = EvolutionAPI.check_is_whatsapp(instance, [str(instance.phone_number)])
        if data and "error" not in data:
            contact = data[0] if isinstance(data, list) else data
            instance.whatsapp_jid = contact.get("jid")
            instance.whatsapp_name = contact.get("name", "")

            # Agora busca a foto de perfil
            profile_pic = EvolutionAPI.fetch_profile_pic(
                instance,
                str(instance.phone_number),
            )
            if isinstance(profile_pic, str):  # Se for uma URL válida
                instance.whatsapp_profile_pic = profile_pic

            instance.save()
