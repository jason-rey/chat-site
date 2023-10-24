from server_commands import CommandInterface
from room_logic import User
from room_logic import Room

class DisconnectFromRoom(CommandInterface):
    def __init__(self, users:dict[str, User]={}, rooms:dict[str, Room]={}):
        self.users = users
        self.rooms = rooms
    
    async def execute(self, roomName:str="", username:str=""):
        if roomName == "" or username == "":
            raise Exception("invalid arguments")
        
        if roomName not in self.rooms or username not in self.users:
            raise Exception("room or username does not exist")
        
        roomObj = self.rooms[roomName]
        userObj = self.users[username]

        if username not in roomObj.connectedUsers:
            print("not in room")
            return

        await roomObj.disconnect_user(userObj)
        userObj.currentRoom = None

        Response = await self.create_response(status="200")
        return Response

