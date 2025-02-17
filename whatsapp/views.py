# Create your views here.
from django.conf import settings
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import WhatsAppInstance
from .serializers import WhatsAppInstanceSerializer
from .services import EvolutionAPI


class WhatsAppInstanceViewSet(viewsets.ModelViewSet):
    """API para gerenciar instâncias do WhatsApp"""

    serializer_class = WhatsAppInstanceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Retorna apenas as instâncias do usuário autenticado"""
        return WhatsAppInstance.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Vincula a instância ao usuário autenticado"""
        serializer.save(user=self.request.user)


class SyncInstancesView(APIView):
    """Sincroniza instâncias do WhatsApp da Evolution API para o Django"""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = EvolutionAPI.get_instances()

        if "error" in data:
            return Response({"error": data["error"]}, status=400)

        # Salvar instâncias no banco local
        for instance in data.get("instances", []):
            WhatsAppInstance.objects.update_or_create(
                instance_name=instance["name"],
                phone_number=instance["phone"],
                defaults={
                    "api_key": settings.EVOLUTION_API_KEY,
                    "is_active": instance["status"] == "active",
                },
            )

        return Response({"message": "Instâncias sincronizadas com sucesso!"})
