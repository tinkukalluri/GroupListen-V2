from itertools import count
import json
from channels.generic.websocket import AsyncWebsocketConsumer
import string
import random
from api import models
from django.contrib.auth.models import User
from rest_framework.views import APIView


def getList(dict):
        return list(dict.keys())

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self ):
        #print("connected to websocket")
        await self.accept()
        await self.send(text_data=json.dumps({
            "conn_status":True,
        }))
    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.my_room_group_name,
            self.channel_name
        )


    # Receive message from WebSocket
    # _count=1
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        # if(self._count==1):
        # Join room group
        if text_data_json.get('user_id')!=None and text_data_json.get('room_code')!=None:
            #print(text_data_json.get('room_code'))
            self.my_room_group_name=str(text_data_json["room_code"])
            self.user_id=text_data_json["user_id"]
            #print("self.my_room_group_name***********"+str(self.my_room_group_name),self.user_id)
            await self.channel_layer.group_add(
            self.my_room_group_name,
            self.channel_name
                )
        else:
            #print(text_data_json)
            msg_id=getList(text_data_json)[0]
            text = text_data_json[msg_id]['text']
            user_id=text_data_json[msg_id]['msg_from']
            room_id=text_data_json[msg_id]['room_id']
            # Send message to room group
            await self.channel_layer.group_send(
                self.my_room_group_name,
                {
                    'type': 'chat_message',
                    **text_data_json
                }
            )

    # Receive message from room group
    async def chat_message(self, event):
        #print("message from room group",event)
        # Send message to WebSocket
        await self.send(text_data=json.dumps(
            event
        ))