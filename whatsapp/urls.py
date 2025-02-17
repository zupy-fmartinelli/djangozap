from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import WhatsAppInstanceViewSet

router = DefaultRouter()
router.register(r"instances", WhatsAppInstanceViewSet, basename="whatsapp-instance")

urlpatterns = [
    path("", include(router.urls)),
]
