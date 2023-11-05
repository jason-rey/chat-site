from .command_interface import CommandInterface
from room_logic import User
from room_logic import Room

class ConnectToRoom(CommandInterface):
    def __init__(self, actionName:str="", users:dict[str, User]={}, rooms:dict[str, Room]={}):
        super().__init__(actionName=actionName)
        self.users = users
        self.rooms = rooms
    
    async def execute(self, username:str="", roomName:str=""):
        if username == "" or roomName == "":
            return await self.create_response(
                self.responseStatusEnum.ERROR, 
                type="input_error", 
                data={"message": "invalid arguments to ConnectToRoom"}
            )
        
        if roomName not in self.rooms:
            return await self.create_response(
                self.responseStatusEnum.ERROR,
                type="input_error",
                data={"message": f"{roomName} does not exist"}
            )
        
        targetRoom = self.rooms[roomName]
        await targetRoom.connect_user(self.users[username])
        self.users[username].currentRoom = targetRoom
        connectedUsernames = await targetRoom.getConnectedUsernames()
        
        return await self.create_response(
            self.responseStatusEnum.OK, 
            type=self.actionName,
            data={"roomName": roomName, "usernames": connectedUsernames}
        )