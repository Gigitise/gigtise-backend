import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async

from .models import User
from .signals import new_order_created

class OrderConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        print(self.room_id)

        if self.room_id:
            self.room_group_name = f"order_{self.room_id}"
            await (self.channel_layer.group_add)(
                self.room_group_name, self.channel_name
            )
            await self.accept()

            print("WS Connected")
            print(f"{self.room_group_name} created")
        
        else:
            await self.close()
        
        # self.user = self.scope['user']                

        # Join room group    
    async def new_order(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
                'type':'new_order',
                "message": message
            }
        ))

        
        # print(f'Room name => {self.room_id}\nRoom group => {self.room_group_name}')
    
    # async def disconnect(self, code):
    #     await (self.channel_layer.group_discard)(
    #         self.room_group_name, self.channel_name
    #     )
    #     return super().disconnect(code)
    
    # async def receive(self, text_data):
    #     data = json.loads(text_data)
    #     message_type = data.get('type')

    #     if message_type == 'new.order':
    #         self.room_name = data.get('room_name')
    #         print(self.room_name)
    #         await self.channel_layer.group_add(
    #             self.room_name, self.channel_name
    #         )
    
    # async def receive(self, text_data=None, bytes_data=None):
    #     text_data_json = await json.loads(text_data)
    #     message = await text_data_json['message']
    #     print(message)

    #      # Send message to room group
    #     await async_to_sync(self.channel_layer.group_send)(
    #         self.room_group_name, {"type": "chat.message", "message": message}
    #     )
