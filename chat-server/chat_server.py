import asyncio
import websockets
from websockets.server import WebSocketServerProtocol
import json

import utils
import room_logic
from server_commands import *
from config import Config

class Server():
    def __init__(self, _ip, _port):
        self.ip = _ip
        self.port = _port

        self.authenticator = utils.Authenticator(Config.AUTH_SERVER_IP, Config.AUTH_SERVER_PORT)
        if not issubclass(type(self.authenticator), utils.AuthenticatorInterface):
            raise Exception("Authenticator does not implement expected interface")

        # {username : User()}
        self.users: dict[str, room_logic.User] = {}

        # {roomName : Room()}
        self.rooms: dict[str, room_logic.Room] = {}
        
        # commands are found in the /server_commands directory
        self.commands: dict[str, CommandInterface] = {
            "get_rooms": GetRooms(actionName="get_rooms", rooms=self.rooms),
            "connect_to_room": ConnectToRoom(actionName="connect_to_room", users=self.users, rooms=self.rooms),
            "disconnect_from_room": DisconnectFromRoom(users=self.users, rooms=self.rooms),
            "create_room": CreateRoom(rooms=self.rooms),
            "send_message": SendMessage(rooms=self.rooms)
        }

    async def start(self):
        print(f"[STARTING] server has started")
        print(f"[LISTENING] listening on address {self.ip}:{self.port}")
        async with websockets.serve(self.handle_connection, self.ip, self.port):
            await asyncio.Future()

    async def handle_connection(self, websocket: WebSocketServerProtocol):
        addr = websocket.remote_address[0]
        port = websocket.remote_address[1]
        data = await websocket.recv()
        connectionInfo = json.loads(data)
        username = connectionInfo["username"]
        print(f"[CONNECTION] {username} ({addr}:{port}) has connected")

        newUser = room_logic.User(
            username=username, 
            addr=addr, 
            port=port, 
            socket=websocket
        )
        self.users[username] = newUser
        await self.main_loop(newUser)
    
    async def main_loop(self, user: room_logic.User):
        while True:
            try:
                message = await user.socket.recv()
                command = json.loads(message)

                givenToken = command["token"]
                isValid = await self.authenticator.check(user, givenToken)
                if not isValid:
                    raise Exception("token is invalid")

                result = await self.execute_command(command)    
                await user.socket.send(result.to_json())
            except Exception as e:
                print(e)
                print(f"[DISCONNECTION] {user.name} ({user.addr}:{user.port}) has disconnected")
                self.users.pop(user.name)
                if user.currentRoom != None:
                    await user.currentRoom.disconnect_user(user)
                break
                
    async def execute_command(self, commandMessage: str) -> utils.Response:
        """"
            command format:
            {
                "token": the user's authentication token,
                "action": the command name,
                "args": command arguments in json
            }
        """

        CommandObj = self.commands[commandMessage["action"]]
        return await CommandObj.execute(**commandMessage["args"])

if __name__ == "__main__":
    server = Server(Config.HOST_IP, Config.HOST_PORT)
    asyncio.run(server.start())
