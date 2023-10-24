from server_commands import CommandInterface
from room_logic import Room

class SendMessage(CommandInterface):
    def __init__(self, rooms:[str, Room]={}):
        self.rooms = rooms

    async def execute(self, roomName:str="", author:str="", message:str=""):
        targetRoom = self.rooms[roomName]
        await targetRoom.send_message_to_connected_users(author, message)

        Response = await self.create_response("200")
        return Response