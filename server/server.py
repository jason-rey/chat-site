import asyncio
import websockets
import socket

class Server():
    def __init__(self):
        self.server = None
        self.connections = {}

    async def start(self):
        ip = socket.gethostbyname(socket.gethostname())
        print(ip)
        port = 5050
        print(f"[STARTING] server has started")
        print(f"[LISTENING] listening on port {port}")

        async with websockets.serve(self.handle_connection, ip, port):
            await asyncio.Future()

    async def handle_connection(self, websocket):
        addr = websocket.remote_address[0]
        print(f"[CONNECTION] {addr} has connected")

        self.connections[addr] = websocket
        print(f"[ACTIVE CONNECTIONS] {len(self.connections)}")

        await self.on_message_receive(websocket)

    async def on_message_receive(self, websocket):
        authorAddr = websocket.remote_address[0]
        while True:
            try:
                message = await websocket.recv()
                for addr in self.connections:
                    ws = self.connections[addr]
                    await ws.send(f"{authorAddr}: {message}")
            except Exception as e:
                print(f"[DISCONNECTION] {authorAddr} has disconnected")
                self.connections.pop(authorAddr)
                print(f"[ACTIVE CONNECTIONS] {len(self.connections)}")
                break


server = Server()

asyncio.run(server.start())
