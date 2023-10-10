import random
import asyncio
import websockets

from message import Message
from user import User
from response import Response

class Room():
    def __init__(self, roomName):
        self._name = roomName
        self.connectedUsers = {}
        self.messages = []

    @property
    def name(self):
        return self._name
    
    @property
    def numberOfConnections(self):
        return len(self.connectedUsers)
    
    def getConnectedUsernames(self):
        out = []
        for user in self.connectedUsers:
            out.append(user)

        return out

    async def send_message(self, target: User, message: Message):
        msgData = {
            "author": message.author,
            "message": message.contents
        }
        
        outMsg = Response("200", "receive_message", msgData)
        await target.socket.send(outMsg.to_json())
        
    async def connect_user(self, user: User):
        self.connectedUsers[user.name] = user
        
        for message in self.messages:
            await self.send_message(user, message)

    async def disconnect_user(self, user: User):
        self.connectedUsers.pop(user.name)

    async def send_message_to_connected_users(self, author, message):
        messageObj = Message(author, message)
        for username in self.connectedUsers:
            targetUser = self.connectedUsers[username]
            await self.send_message(targetUser, messageObj)
        self.messages.append(messageObj)
    
