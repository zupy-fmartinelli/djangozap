# Register your models here.
from django.contrib import admin

from .models import WhatsAppInstance


@admin.register(WhatsAppInstance)
class WhatsAppInstanceAdmin(admin.ModelAdmin):
    list_display = ("instance_name", "phone_number", "is_active", "created_at")
    search_fields = ("instance_name", "phone_number")
    list_filter = ("is_active",)
