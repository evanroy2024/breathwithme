import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Get the chatroom name from the URL
        self.chatroom_name = self.scope['url_route']['kwargs']['chatroom_name']
        self.room_group_name = f'chatroom_{self.chatroom_name}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Accept WebSocket connection
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json['action']
        
        if action == 'play_song':
            song_url = text_data_json['song_url']
            song_title = text_data_json['song_title']
            song_artist = text_data_json['song_artist']

            # Broadcast to all users in the group (everyone in the room)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'play_song',
                    'song_url': song_url,
                    'song_title': song_title,
                    'song_artist': song_artist,
                }
            )

        elif action == 'pause_song':
            # Broadcast pause event to all users in the room
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'pause_song',
                }
            )

    # Handle play song event (broadcast to WebSocket)
    async def play_song(self, event):
        song_url = event['song_url']
        song_title = event['song_title']
        song_artist = event['song_artist']

        # Send the play song action to the WebSocket
        await self.send(text_data=json.dumps({
            'action': 'play_song',
            'song_url': song_url,
            'song_title': song_title,
            'song_artist': song_artist,
        }))

    # Handle pause song event (broadcast to WebSocket)
    async def pause_song(self, event):
        # Send the pause song action to the WebSocket
        await self.send(text_data=json.dumps({
            'action': 'pause_song',
        }))
