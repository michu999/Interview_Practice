from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AIModelLogViewSet

router = DefaultRouter()
router.register(r'logs', AIModelLogViewSet)

urlpatterns = [
    path('', include(router.urls)),
]