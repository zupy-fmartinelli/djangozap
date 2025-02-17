# Create your views here.
from rest_framework import permissions
from rest_framework import viewsets

from .models import WhatsAppInstance
from .serializers import WhatsAppInstanceSerializer


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
