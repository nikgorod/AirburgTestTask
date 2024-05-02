import json
from channels.generic.websocket import AsyncConsumer


class Consumer(AsyncConsumer):

    async def websocket_connect(self):
        await self.send({"type": "websocket.accept"})

    async def websocket_disconnect(self, close_code):
        pass

    async def websocket_receive(self, text_data):
        await self.send({
            "type": "websocket.send",
            "text": "Hello from Django socket"
        })
