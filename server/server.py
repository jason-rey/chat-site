import asyncio
import websockets
import socket

class Server():
    def __init__(self):
        self.server = None
        self.connections = {}

    async def start(self):
        ip = socket.gethostbyname(socket.gethostname())
        port = 5050
        print(f"[STARTING] server has started")

        async with websockets.serve(self.handle_connection, ip, port):
            await asyncio.Future()
        
        print(f"[LISTENING] listening on port {port}")

    async def handle_connection(self, websocket):
        addr = websocket.remote_address[0]
        print(f"[CONNECTION] {addr} has connected")

        self.connections[addr] = websocket
        print(f"[ACTIVE CONNECTIONS] {len(self.connections)}")

        await self.on_message_receive(websocket)

    async def on_message_receive(self, websocket):
        while True:
            try:
                message = await websocket.recv()
                for addr in self.connections:
                    ws = self.connections[addr]
                    await ws.send(message)
            except Exception as e:
                addr = websocket.remote_address[0]
                print(f"[DISCONNECTION] {addr} has disconnected")
                self.connections.pop(addr)
                print(f"[ACTIVE CONNECTIONS] {len(self.connections)}")
                break


server = Server()

asyncio.run(server.start())
