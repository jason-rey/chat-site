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
        port = websocket.remote_address[1]
        print(f"[CONNECTION] {addr}:{port} has connected")


        if addr not in self.connections:
            self.connections[addr] = {port: websocket}
        else:
            self.connections[addr][port] = websocket
        await self.on_message_receive(websocket)

    async def on_message_receive(self, websocket):
        authorAddr = websocket.remote_address[0]
        authorPort = websocket.remote_address[1]
        while True:
            try:
                message = await websocket.recv()
                for addr in self.connections:
                    for port in self.connections[addr]:
                        ws = self.connections[addr][port]
                        await ws.send(f"{authorPort}: {message}")
            except Exception as e:
                print(e)
                print(f"[DISCONNECTION] {authorAddr}:{authorPort} has disconnected")
                self.connections[authorAddr].pop(authorPort)

                if len(self.connections[authorAddr]) <= 0:
                    self.connections.pop(authorAddr)
                
                print(f"[ACTIVE CONNECTIONS] {len(self.connections)}")
                break


server = Server()

asyncio.run(server.start())
