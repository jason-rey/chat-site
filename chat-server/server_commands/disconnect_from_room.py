from asyncio import sleep, create_task
import time

from .command_interface import CommandInterface
from room_logic import User
from room_logic import Room

class DisconnectFromRoom(CommandInterface):
    def __init__(self, users:dict[str, User]={}, rooms:dict[str, Room]={}):
        self.users = users
        self.rooms = rooms
    
    async def delayRoomDestruction(self, roomName:str, timeoutTime:int):
        if roomName not in self.rooms:
            return
        checkDelay = 0.25
        start = time.time()
        curr = start
       
        while (curr - start) < timeoutTime:
            if self.rooms[roomName].numberOfConnections > 0:
                return  
            await sleep(checkDelay)
            curr = time.time()

        self.rooms.pop(roomName)

    async def execute(self, roomName:str="", username:str=""):
        if roomName == "" or username == "":
            return await self.create_response(
                self.responseStatusEnum.ERROR,
                type="input_error",
                data={"message": "invalid arguments for DisconnectFromRoom"}
            )
        
        if roomName not in self.rooms or username not in self.users:
            return await self.create_response(
                self.responseStatusEnum.ERROR,
                type="input_error",
                data={"message": "give room or username does not exist"}
            )
        
        roomObj = self.rooms[roomName]
        userObj = self.users[username]

        if username not in roomObj.connectedUsers:
            return await self.create_response(
                self.responseStatusEnum.ERROR,
                type="input_error",
                data={"message": "user not connected to room"}
            )

        await roomObj.disconnect_user(userObj)
        userObj.currentRoom = None
        
        if roomObj.numberOfConnections <= 0:
            create_task(self.delayRoomDestruction(roomName, 60))

        return await self.create_response(self.responseStatusEnum.OK)

