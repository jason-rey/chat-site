#!/usr/bin/python3

import asyncio
import websockets
from dotenv import load_dotenv
import os
import json

from room import Room
from user import User
from response import Response

'''
TODO
    change response and command data to use json instead of what it is rn
    change status codes to use normal http status codes
    (do the same for the authentication server too)
'''

class Server():
    def __init__(self, _ip, _port):
        self.ip = _ip
        self.port = _port
        self.authServerSocket = None

        # {username : User()}
        self.usersNotInRooms = {}

        # {username : Room()}
        self.usersInRooms = {}

        self.rooms = {}

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
                message = await user.socket.recv()
                print(f"command: {message}")
                command = json.loads(message)
                result = await self.execute_command(command)

                # print(f"{user.addr}: {action} : {str(result)}")
                print(f"result: {result.to_json()}")
                await user.socket.send(result.to_json())
                print()

            except Exception as e:
                print(e)
                print(f"[DISCONNECTION] {user.name} ({user.addr}:{user.port}) has disconnected")
                if user.name in self.usersInRooms:
                    await self.usersInRooms[user.name].disconnect_user(user)
                    self.usersInRooms.pop(user.name)
                elif user.name in self.usersInRooms:
                    self.usersNotInRooms.pop(user.name)
                    
                break
                
    async def send_past_messages(self, target):
        for message in self.pastMessages:
            await target.send(message)

    async def execute_command(self, command):
        """"
            command format:
            {
                "username": "username",
                "sessionID": "sessionID",
                "action": "action",
                "args": {}
            }
        """

        method = self.commands[command["action"]]
        return await method(**command["args"])
    
    async def get_rooms(self):
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
                    "rooms": "roomName1,numberOfConnected|...|"
                }
            }
        '''

        roomDataString = ""
        for roomName in self.rooms:
            room = self.rooms[roomName]
            roomDataString += f"|{room.name},{room.numberOfConnections}"

        return Response("200", "get_rooms", {"rooms": roomDataString[1:]})

    async def connect_to_room(self, username=None, roomName=None):
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

        user = self.usersNotInRooms.pop(username)
        self.usersInRooms[user.name] = self.rooms[roomName]
        await self.rooms[roomName].connect_user(user)

        connectedUsersString=""
        for username in self.rooms[roomName].getConnectedUsernames():
            connectedUsersString += f"|{username}"

        if connectedUsersString != "":
            connectedUsersString = connectedUsersString[1:]

        return Response("200", "connect_to_room", {"connectedUsers": connectedUsersString})
    
    async def disconnect_from_room(self, roomName=None, username=None):
        room = self.rooms[roomName]
        userObj = room.connectedUsers[username]
        await room.disconnect_user(userObj)
        self.usersNotInRooms[username] = userObj
        
        return Response("200")

    async def create_room(self, roomName=None, username=None):
        newRoom = Room(roomName)
        self.rooms[roomName] = newRoom

        return Response("200")
    
    async def send_message(self, roomName=None, author=None, message=None):
        targetRoom = self.rooms[roomName]
        await targetRoom.send_message_to_connected_users(author, message)
        
        return Response("200")

def configure():
    load_dotenv()

if __name__ == "__main__":
    configure()
    server = Server(os.getenv("chat_server_local_ip"), os.getenv("chat_server_port"))
    asyncio.run(server.start())
