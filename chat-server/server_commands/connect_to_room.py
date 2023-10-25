from server_commands import CommandInterface
from room_logic import User
from room_logic import Room

class ConnectToRoom(CommandInterface):
    def __init__(self, actionName:str="", users:dict[str, User]={}, rooms:dict[str, Room]={}):
        super().__init__(actionName=actionName)
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
                    "connectedUsers: "["user1", "user2", ...]"
                }
            }
        '''
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
            data={"usernames": connectedUsernames}
        )