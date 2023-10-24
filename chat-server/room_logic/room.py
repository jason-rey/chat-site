from room_logic.message import Message
from room_logic.user import User

import utils

class Room():
    def __init__(self, roomName:str):
        self._name = roomName
        self.connectedUsers: dict[str, User] = {}
        self.messages: list[Message] = []

    @property
    def name(self) ->str:
        return self._name
    
    @property
    def numberOfConnections(self) -> int:
        return len(self.connectedUsers)
    
    def getConnectedUsernames(self) -> list[str]:
        out = []
        for user in self.connectedUsers:
            out.append(user)

        return out

    async def send_message(self, target: User, message: Message):
        msgData = {
            "author": message.author,
            "message": message.contents
        }
        
        outMsg = utils.Response("200", "receive_message", msgData)
        await target.socket.send(outMsg.to_json())
        
    async def connect_user(self, user: User):
        self.connectedUsers[user.name] = user
        for message in self.messages:
            await self.send_message(user, message)

        await self.send_message_to_connected_users("[Room]", f"{user.name} has connected.")

    async def disconnect_user(self, user: User):
        self.connectedUsers.pop(user.name)
        await self.send_message_to_connected_users("[Room]", f"{user.name} has disconnected.")

    async def send_message_to_connected_users(self, author:str , message: str):
        messageObj = Message(author, message)
        for username in self.connectedUsers:
            targetUser = self.connectedUsers[username]
            await self.send_message(targetUser, messageObj)
        self.messages.append(messageObj)
    
