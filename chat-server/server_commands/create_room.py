from server_commands import CommandInterface
from room_logic import Room

class CreateRoom(CommandInterface):
    def __init__(self, rooms:[str, Room]={}):
        self.rooms = rooms

    async def execute(self, roomName:str="", username:str=""):
        if roomName == "" or username == "":
            return await self.create_response(
                status=self.responseStatusEnum.ERROR,
                type="input_error",
                data={"message": "invalid arguments to CreateRoom"}
            )
        
        self.rooms[roomName] = Room(roomName)

        return await self.create_response(status=self.responseStatusEnum.OK)