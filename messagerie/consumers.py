import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.db.models import Q
from .models import Conversation, Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.conv_id = self.scope['url_route']['kwargs']['conv_id']
        self.room_group_name = f'conversation_{self.conv_id}'
        self.user = self.scope['user']

        if not self.user.is_authenticated or not await self._user_in_conversation():
            await self.close()
            return

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        contenu = data.get('content', '').strip()
        if not contenu:
            return

        message = await self._create_message(contenu)
        event = {
            'type': 'chat.message',
            'message': message.contenu,
            'expediteur': self.user.nom_complet(),
            'date_envoi': message.date_envoi.strftime('%H:%M'),
            'message_id': message.id,
            'expediteur_id': self.user.id,
        }
        await self.channel_layer.group_send(self.room_group_name, event)

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'expediteur': event['expediteur'],
            'date_envoi': event['date_envoi'],
            'message_id': event['message_id'],
            'expediteur_id': event['expediteur_id'],
        }))

    @database_sync_to_async
    def _user_in_conversation(self):
        return Conversation.objects.filter(
            Q(utilisateur1=self.user) | Q(utilisateur2=self.user),
            id=self.conv_id
        ).exists()

    @database_sync_to_async
    def _create_message(self, contenu):
        conversation = Conversation.objects.get(id=self.conv_id)
        return Message.objects.create(
            conversation=conversation,
            expediteur=self.user,
            contenu=contenu
        )
