from django.shortcuts import render
from django.http import HttpResponse
from .models import AIModelLog
from .serializers import AIModelLogSerializer
from rest_framework import viewsets

# Create your views here.
class AIModelLogViewSet(viewsets.ModelViewSet):
    queryset = AIModelLog.objects.all().order_by('-timestamp')
    serializer_class = AIModelLogSerializer