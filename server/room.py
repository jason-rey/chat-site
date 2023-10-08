import random
import asyncio

from message import Message
from user import User

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

    async def connect_user(self, user: User):
        self.connectedUsers[user.name] = user

        for message in self.messages:
            outMsg = f"1|receive_message|{message.author}|{message.contents}"
            await user.socket.send(outMsg)

    async def disconnect_user(self, user: User):
        self.connectedUsers.pop(user.name)

    async def send_message_to_connected_users(self, author, message):
        for username in self.connectedUsers:
            user = self.connectedUsers[username]
            outMsg = f"1|receive_message|{author}|{message}"
            await user.socket.send(outMsg)

        self.messages.append(Message(author, message))
    
