import asyncio
import websockets
from dotenv import load_dotenv
import os

from room import Room
from user import User

class Server():
    def __init__(self, _ip, _port):
        self.ip = _ip
        self.port = _port

        # {username : User()}
        self.usersNotInRooms = {}

        # {username : Room()}
        self.usersInRooms = {}

        self.rooms = {
            "First" : Room("First"),
            "Second" : Room("Second"),
            "Room 3" : Room("Room 3")
        }

        self.commands = {
            "get_rooms" : self.get_rooms,
            "connect_to_room" : self.connect_to_room,
            "disconnect_from_room" : self.disconnect_from_room,
            "create_room" : self.create_room,
            "send_message" : self.send_message
        }

    async def start(self):
        print(f"[STARTING] server has started")
        print(f"[LISTENING] listening on address {self.ip}:{self.port}")

        async with websockets.serve(self.handle_connection, self.ip, self.port):
            await asyncio.Future()
	
    async def send_past_messages(self, target):
        for message in self.pastMessages:
            await target.send(message)

    async def handle_connection(self, websocket):
        addr = websocket.remote_address[0]
        port = websocket.remote_address[1]
        username = await websocket.recv()

        print(f"[CONNECTION] {username} ({addr}:{port}) has connected")
        newUser = User(username, addr, port, websocket)
        self.usersNotInRooms[username] = newUser
        await self.main_loop(newUser)
    
    async def main_loop(self, user: User):
        while True:
            try:
                command = await user.socket.recv()
                command = await self.parse_command(command)
                result = await self.execute_command(command)
                while result is None:
                    await asyncio.sleep(0.5)

                action = command["method"]
                print(f"{user.addr}: {action} : {str(result)}")
                await user.socket.send(str(result))
            except:
                print(f"[DISCONNECTION] {user.name} ({user.addr}:{user.port}) has disconnected")
                if user.name in self.usersInRooms:
                    targetUser = self.usersInRooms[user.name]
                    await self.usersInRooms[user.name].disconnect_user(targetUser)
                else:
                    self.usersNotInRooms.pop(user.name)
                    
                break
            
    
    async def parse_command(self, command):
        parsed = {
            "method" : "",
            "args": []
        }

        delimiter = "|"
        command = command.split(delimiter)
        parsed["method"] = command[0]
        parsed["args"] = command[1:]

        return parsed

    async def execute_command(self, command):
        # commands return a Response object that contain a status code and data
        # status codes are:
        #   0 : failure
        #   1 : success
        
        # see methods for specifics on data output

        # should decrypt command argument here

        method = self.commands[command["method"]]
        return await method(*command["args"])
    
    async def get_rooms(self, *args):
        response = "get_rooms"
        for roomName in self.rooms:
            room = self.rooms[roomName]
            response += f"|{room.name},{room.numberOfConnections}"
            
        return f"1|{response}"

    async def connect_to_room(self, *args):
        # connect_to_room|username|roomName|
        # response: status_code|connect_to_room|connectedUser1|connectedUser2...
        response = "connect_to_room"
        user = self.usersNotInRooms.pop(args[0])
        self.usersInRooms[user.name] = user
        targetRoom = args[1]
        await self.rooms[targetRoom].connect_user(user)

        for username in self.rooms[targetRoom].getConnectedUsernames():
            response += f"|{username}"

        return f"1|{response}"
    
    async def disconnect_from_room(self, *args):
        pass

    async def create_room(self, *args):
        pass
    
    async def send_message(self, *args):
        # send_message|roomName|username|"messageContents"
        targetRoom = self.rooms[args[0]]
        author = args[1]
        messageContents = args[2]
        
        await targetRoom.send_message_to_connected_users(author, messageContents)
        return "1|"

    # async def on_message_receive(self, websocket):
    #     authorAddr = websocket.remote_address[0]
    #     authorPort = websocket.remote_address[1]
    #     while True:
    #         try:
    #             message = await websocket.recv()
    #             self.pastMessages.append(outMsg)
    #             for addr in self.connections:
    #                 for port in self.connections[addr]:
    #                     ws = self.connections[addr][port][1]
    #                     username = self.connections[authorAddr][authorPort][0]
    #                     outMsg = f"{username}: {message}"
    #                     await ws.send(outMsg)
    #         except Exception as e:
    #             print(e)
    #             print(f"[DISCONNECTION] {self.connections[authorAddr][authorPort][0]} ({authorAddr}:{authorPort}) has disconnected")
    #             self.connections[authorAddr].pop(authorPort)

    #             if len(self.connections[authorAddr]) <= 0:
    #                 self.connections.pop(authorAddr)
                
    #             print(f"[ACTIVE CONNECTIONS] {self.get_number_of_connections()}")
    #             break

def configure():
    load_dotenv()

if __name__ == "__main__":
    configure()
    server = Server(os.getenv("chat_server_local_ip"), os.getenv("chat_server_port"))
    asyncio.run(server.start())
