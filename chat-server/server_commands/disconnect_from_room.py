from server_commands import CommandInterface
from room_logic import User
from room_logic import Room

class DisconnectFromRoom(CommandInterface):
    def __init__(self, users:dict[str, User]={}, rooms:dict[str, Room]={}):
        self.users = users
        self.rooms = rooms
    
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

        return await self.create_response(self.responseStatusEnum.OK)

