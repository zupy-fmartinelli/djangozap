from django.contrib import admin
from django.contrib import messages
from django.core.management import call_command
from django.shortcuts import redirect
from django.urls import path
from django.utils.html import format_html

from .models import WhatsAppInstance
from .services import EvolutionAPI


@admin.register(WhatsAppInstance)
class WhatsAppInstanceAdmin(admin.ModelAdmin):
    list_display = (
        "instance_name",
        "phone_number",
        "integration_type",
        "is_active",
        "created_at",
        "show_qr_code",
    )
    search_fields = ("instance_name", "phone_number")
    list_filter = ("is_active", "integration_type")
    readonly_fields = ("api_key", "token", "qrcode_url", "created_at", "updated_at")

    def get_urls(self):
        """Adiciona URLs personalizadas para sincronizar e criar instâncias"""
        urls = super().get_urls()
        custom_urls = [
            path(
                "sync/",
                self.admin_site.admin_view(self.sync_instances),
                name="whatsapp_sync",
            ),
            path(
                "create-instance/",
                self.admin_site.admin_view(self.create_instance),
                name="whatsapp_create_instance",
            ),
        ]
        return custom_urls + urls

    def sync_instances(self, request):
        """Executa a sincronização das instâncias e redireciona para a lista"""
        call_command("sync_instances")
        self.message_user(
            request,
            "✅ Instâncias sincronizadas com sucesso!",
            messages.SUCCESS,
        )
        return redirect("..")

    def create_instance(self, request):
        """Cria uma nova instância no Evolution API e exibe QR Code"""

        instance_count = WhatsAppInstance.objects.count() + 1
        instance_name = f"instancia-{instance_count}"
        integration_type = request.GET.get(
            "integration",
            "WHATSAPP-BAILEYS",
        )  # Define um padrão

        result = EvolutionAPI.create_instance(instance_name, integration_type)

        if "error" in result:
            self.message_user(
                request,
                f"❌ Erro ao criar instância: {result['error']}",
                messages.ERROR,
            )
            return redirect("..")

        WhatsAppInstance.objects.create(
            instance_name=instance_name,
            integration_type=integration_type,
            api_key=result.get(
                "api_key",
                "",
            ),  # 🔥 Agora a API Key é salva automaticamente
            token=result.get("token", ""),
            qrcode_url=result.get("qrcode_url", ""),
            is_active=False,
        )

        self.message_user(
            request,
            f"✅ Instância '{instance_name}' criada com sucesso!",
            messages.SUCCESS,
        )
        return redirect("..")

    def changelist_view(self, request, extra_context=None):
        """Adiciona os botões na tela de listagem"""
        extra_context = extra_context or {}
        extra_context["sync_button_url"] = "sync/"
        extra_context["create_instance_url"] = "create-instance/"
        return super().changelist_view(request, extra_context=extra_context)

    @admin.display(
        description="QR Code",
    )
    def show_qr_code(self, obj):
        """Exibe o QR Code no Django Admin"""
        if obj.qrcode_url:
            return format_html(f'<img src="{obj.qrcode_url}" width="150">')
        return "QR Code não disponível"
