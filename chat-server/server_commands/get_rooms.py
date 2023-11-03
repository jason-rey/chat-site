from .command_interface import CommandInterface
from room_logic import Room

class GetRooms(CommandInterface):
    def __init__(self, actionName="", rooms:dict[str, Room]={}):
        self.actionName = actionName
        self.rooms = rooms

    async def execute(self):
        roomDataDict = {}
        for roomName in self.rooms:
            currRoom = self.rooms[roomName]
            roomDataDict[roomName] = {
                "connectedCount": currRoom.numberOfConnections
            } 

        return await self.create_response(
            self.responseStatusEnum.OK,
            type=self.actionName,
            data={"rooms": roomDataDict}
        )