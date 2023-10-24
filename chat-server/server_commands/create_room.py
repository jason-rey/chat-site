from server_commands import CommandInterface
from room_logic import Room

class CreateRoom(CommandInterface):
    def __init__(self, rooms:[str, Room]={}):
        self.rooms = rooms

    async def execute(self, roomName:str="", username:str=""):
        if roomName == "" or username == "":
            raise Exception("invalid arguments to CreateRoom")
        
        self.rooms[roomName] = Room(roomName)

        Response = await self.create_response(status="200")
        return Response