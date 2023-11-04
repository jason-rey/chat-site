from websockets.server import WebSocketServerProtocol

class User():
    def __init__(self, username:str="", addr:str="", port:str="", socket:WebSocketServerProtocol=None):
        self._name = username
        self._addr = addr
        self._port = port
        self._socket = socket
        self.currentRoom = None

    @property
    def name(self) -> str:
        return self._name

    @property
    def addr(self) -> str:
        return self._addr

    @property
    def port(self) -> str:
        return self._port

    @property
    def socket(self) -> WebSocketServerProtocol:
        return self._socket