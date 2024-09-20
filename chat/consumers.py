import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, JsonWebsocketConsumer

class ChatConsumer(JsonWebsocketConsumer):
    print('____________________')
    print('ChatConsumer class entered.')

    def connect(self):
        print('Connecting...')
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        print('Connection finished.')
        self.accept()

    def disconnect(self, close_code):
        print('Disconnecting...')
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        print('Disconnection complete.')

    # Receive message from WebSocket
    def receive_json(self, text_data):
        print('Received message from websocket')
        #print(text_data)
        #text_data_json = json.loads(text_data)
        #message = text_data_json['message']

        # Send message to room group
        # This iteratively performs the 'chat_message' function
        # for every member of the group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'content': text_data
            }
        )
        print('Finished receive function')

    # Receive message from room group
    def chat_message(self, event):
        print('Sending chat_message to room group')
        #print(event)
        message = event['content']
        #print(message)
        # Send message to WebSocket
        self.send_json(message)
        print('Finished chat message')