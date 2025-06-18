from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AIModelLogViewSet

# Create a router and register our viewset with it.
router = DefaultRouter()
router.register(r'ai_model_logs', AIModelLogViewSet, basename='ai_model_log')
# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
# This will automatically create the following endpoints:
# - `GET /api/ai_model_logs/` - List all AI model logs
# - `POST /api/ai_model_logs/` - Create a new AI model log
# - `GET /api/ai_model_logs/{id}/` - Retrieve a specific AI model log
# - `PUT /api/ai_model_logs/{id}/` - Update a specific AI model log
# - `PATCH /api/ai_model_logs/{id}/` - Partially update a specific AI model log
# - `DELETE /api/ai_model_logs/{id}/` - Delete a specific AI model log
# This setup allows you to easily manage AI model logs through a RESTful API.
