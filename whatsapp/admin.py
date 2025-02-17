from django.contrib import admin
from django.contrib import messages
from django.core.management import call_command
from django.shortcuts import redirect
from django.urls import path

from .models import WhatsAppInstance


@admin.register(WhatsAppInstance)
class WhatsAppInstanceAdmin(admin.ModelAdmin):
    list_display = ("instance_name", "phone_number", "is_active", "created_at")
    search_fields = ("instance_name", "phone_number")
    list_filter = ("is_active",)

    def get_urls(self):
        """Adiciona a URL do botão de sincronização"""
        urls = super().get_urls()
        custom_urls = [
            path(
                "sync/",
                self.admin_site.admin_view(self.sync_instances),
                name="whatsapp_sync",
            ),
        ]
        return custom_urls + urls

    def sync_instances(self, request):
        """Executa a sincronização das instâncias e redireciona para a lista"""
        call_command("sync_instances")
        self.message_user(
            request,
            "Instâncias sincronizadas com sucesso!",
            messages.SUCCESS,
        )
        return redirect("..")

    def changelist_view(self, request, extra_context=None):
        """Adiciona o botão na tela de listagem"""
        extra_context = extra_context or {}
        extra_context["sync_button_url"] = "sync/"  # URL que criamos acima
        return super().changelist_view(request, extra_context=extra_context)
