# myapp/routing.py

from django.urls import path
from .consumers import WebSocketConsumer

websocket_urlpatterns = [
    path('ws/', WebSocketConsumer.as_asgi()),
]
