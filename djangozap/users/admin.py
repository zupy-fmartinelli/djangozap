from allauth.account.decorators import secure_admin_login
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .forms import UserAdminChangeForm
from .forms import UserAdminCreationForm
from .models import User

if settings.DJANGO_ADMIN_FORCE_ALLAUTH:
    admin.autodiscover()
    admin.site.login = secure_admin_login(admin.site.login)  # type: ignore[method-assign]


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            _("Personal info"),
            {
                "fields": (
                    "name",
                    "phone_number",
                    "whatsapp_name",
                    "whatsapp_profile_pic_display",
                    "is_whatsapp",
                ),
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    list_display = [
        "email",
        "name",
        "phone_number",
        "is_whatsapp",
        "whatsapp_profile_pic_display",
        "is_superuser",
    ]
    search_fields = ["name", "email", "phone_number"]
    ordering = ["id"]
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    readonly_fields = ("whatsapp_profile_pic_display", "is_whatsapp")

    @admin.display(
        description="Foto de Perfil",
    )
    def whatsapp_profile_pic_display(self, obj):
        """Exibe a foto de perfil do WhatsApp no Django Admin."""
        if obj.whatsapp_profile_pic:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius: 50%;" />',
                obj.whatsapp_profile_pic,
            )
        return "Sem foto"

    @admin.display(
        description="WhatsApp",
    )
    def is_whatsapp(self, obj):
        """Mostra um ícone se o número for WhatsApp válido."""
        if obj.whatsapp_jid:
            return format_html("✅")  # Ícone indicando que o número tem WhatsApp
        return format_html("❌")  # Ícone indicando que não tem
