"""Websocket consumer for live video chat"""
from channels.generic.websocket import AsyncWebsocketConsumer
import json

class LiveChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'live_chat'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message', '')
        await self.channel_layer.group_send(
            self.room_group_name,
            {'type': 'chat_message', 'message': message}
        )

    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({'message': message}))
