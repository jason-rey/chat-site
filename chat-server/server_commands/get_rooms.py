from .command_interface import CommandInterface
from room_logic import Room

class GetRooms(CommandInterface):
    '''
        command format:
        {
            "action": "get_rooms",
            "args": {}
        }

        response format:
        {
            "statusCode": "200",
            "type": "get_rooms",
            "data": {
                "rooms": {
                    "room1": {"connectedCount": 5}
                    ...
                }
            }
        }
    '''
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