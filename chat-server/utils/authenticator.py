from websockets.sync.client import connect
from response import Response

class Authenticator():
    def __init__(self, _ip, _port):
        self.ip = _ip
        self.port = _port
        self.encryptionKey = ""

    async def check(self, sessionID):
        out = False
        with connect(f"ws://{self.ip}:{self.port}") as websocket:
            websocket.send(f"check|{sessionID}")
            result = await websocket.recv()
            if result == "1":
                out = True

        return out
