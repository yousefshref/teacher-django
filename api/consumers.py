# myapp/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
import os
from django import setup

from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "back.settings")
setup()



from .models import Communicate, GroupMessages, CustomUser
from .serializers import CommunicateSerializer, GroupMessagesSerializer

class WebSocketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        group_id = self.scope['query_string'].decode().split('=')[1]
        group = await self.get_group_messages(group_id)
        ser_group = await self.ser_group_messages(group)
        await self.send(text_data=json.dumps({
            'message': ser_group
        }))


    @database_sync_to_async
    def get_group_messages(self, group_id):
        return GroupMessages.objects.get(id=group_id)

    @database_sync_to_async
    def ser_group_messages(self, group):
        serializer = GroupMessagesSerializer(group)
        return serializer.data['group_communicate']


    async def disconnect(self, close_code):
        # Remove the channel from the group when client disconnects
        for group_id in self.groups:
            await self.channel_layer.group_discard(
                group_id,
                self.channel_name
            )


    async def receive(self, text_data):
        data = json.loads(text_data)
        group_id = data['group']
        user_id = data['user']
        message = data['message']

        # Create a new instance of the Communicate model asynchronously
        group = await self.get_group(group_id)
        user = await self.get_user(user_id)
        communicate_instance = await self.create_communicate_instance(group, user, message)

        # Serialize the updated instance
        serialized_data = await self.serialize_communicate_instance(communicate_instance)

        # Send the serialized data back to the group
        await self.send_group_message(group_id, serialized_data)

    @database_sync_to_async
    def get_group(self, group_id):
        return GroupMessages.objects.get(id=group_id)

    @database_sync_to_async
    def get_user(self, user_id):
        return CustomUser.objects.get(id=user_id)

    @database_sync_to_async
    def create_communicate_instance(self, group, user, message):
        return Communicate.objects.create(group=group, user=user, message=message)

    @database_sync_to_async
    def serialize_communicate_instance(self, communicate_instance):
        serializer = CommunicateSerializer(communicate_instance)
        return serializer.data

    async def send_group_message(self, group_id, message):
        # Send message to the WebSocket group
        await self.channel_layer.group_add(
            group_id,
            self.channel_name
        )
        await self.channel_layer.group_send(
            group_id,
            {
                'type': 'chat.message',
                'message': message
            }
        )

    async def chat_message(self, event):
        # Send the message to the WebSocket
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
