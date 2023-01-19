import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from base.models import User

peers = {}

class ChatConsumer(AsyncWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    

    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "room_%s" % self.room_name

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        peers[self.scope['cookies']['sessionid']] = self

        await self.accept()

    async def disconnect(self, close_code):
        del peers[self.scope['cookies']['sessionid']]

        await self.channel_layer.group_send(
            self.room_group_name, {
                "type": "disconnect_message", 
                "session_id": self.scope['cookies']['sessionid'],
                "username": self.scope['user'].username
            }
        )
        
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data=None):

        text_data_json = json.loads(text_data)

        type = text_data_json.get("type")
        
        if type == "chatting":
        
            message = text_data_json.get("message")
            username = text_data_json.get("username")

            username = await self.retrieve_username(username)

            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name, {
                    "type": "chat_message", 
                    "message": message,
                    "username": username
                }
            )

        elif type == "share_screen":
            await self.channel_layer.group_send(
                self.room_group_name, {
                    "type": "share_screen_message",
                    "totals": len(peers),
                    "sessions": list(peers.keys()),
                    "session_id": text_data_json.get("session_id"),
                    "username": text_data_json.get("username")
                }
            )

        elif type == "join":
            await self.channel_layer.group_send(
                self.room_group_name, {
                    "type": "join_message", 
                    "totals": len(peers),
                    "sessions": list(peers.keys()),
                }
            )

        elif type == "icecandidate":
            candidate = text_data_json.get("candidate")
            session_id = text_data_json.get("session_id")

            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name, {
                    "type": "candidate_message", 
                    "candidate": candidate,
                    "session_id": session_id
                }
            )

        elif type == "offer":
            session_id = text_data_json.get("session_id")

            await peers[session_id].send(text_data=json.dumps({
                "type": 'offer',
                "message": text_data_json.get("signal"),
                "session_id": self.scope['cookies']['sessionid']
            }))

        elif type == "answer":
            session_id = text_data_json.get("session_id")

            await peers[session_id].send(text_data=json.dumps({
                "type": 'answer',
                "message": text_data_json.get("signal"),
                "session_id": self.scope['cookies']['sessionid']
            }))

    async def share_screen_message(self, event):
        await self.send(text_data=json.dumps({
            "type": "share_screen",
            "session_id": event['session_id'],
            "totals": event['totals'],
            "sessions": event['sessions'],
            "username": event['username'],
        }))

    async def join_message(self, event):
        await self.send(text_data=json.dumps({
            "type": "join",
            "session_id": self.scope['cookies']['sessionid'],
            "totals": event['totals'],
            "sessions": event['sessions'],
            "username": self.scope['user'].username,
        }))

    async def disconnect_message(self, event):
        await self.send(text_data=json.dumps({
            "type": "disconnect",
            "session_id": event['session_id'],
            "username": event['username']
        }))

    async def chat_message(self, event):
        message = event["message"]
        username = event["username"]

        await self.send(text_data=json.dumps({
            "type": "chatting",
            "message": message,
            "username": username
        }))

    async def candidate_message(self, event):
        if self.scope['cookies']['sessionid'] != event['session_id']:
            await self.send(text_data=json.dumps({
                "type": "candidate",
                "candidate": event["candidate"],
                "session_id": event['session_id']
            }))
    
    @database_sync_to_async
    def retrieve_username(self, username) -> str:
        try:
            user = User.objects.get(username=username)
            return user.username

        except User.DoesNotExist:
            return "Anonymous"