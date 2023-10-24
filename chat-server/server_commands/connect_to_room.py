from server_commands import CommandInterface
from room_logic import User
from room_logic import Room

class ConnectToRoom(CommandInterface):
    def __init__(self, users:dict[str, User]={}, rooms:dict[str, Room]={}):
        self.users = users
        self.rooms = rooms
    
    async def execute(self, username:str="", roomName:str=""):
        '''
            command format: 
            {
                "action": "connect_to_room",
                "args": {
                    "username": username,
                    "roomName": roomName
                }
            }

            response:
            {
                "statusCode": "200",
                "type": "connect_to_room",
                "data": {
                    "connectedUsers: "user1|user2|user3|...|"
                }
            }
        '''
        if username == "" or roomName == "":
            raise Exception("invalid arguments to ConnectToRoom")
        
        if roomName not in self.rooms:
            print(f"{roomName} doesn't exist")
            return
        
        targetRoom = self.rooms[roomName]
        await targetRoom.connect_user(self.users[username])
        self.users[username].currentRoom = targetRoom

        Response = await self.create_response(status="200", type="connect_to_room")
        return Response