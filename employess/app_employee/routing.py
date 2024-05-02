from django.urls import re_path, path
from app_employee.consumer import Consumer
from channels.routing import ProtocolTypeRouter, URLRouter

websocket_urlpatterns = [
        path('ws/app_employee/', Consumer.as_asgi())
    ]
