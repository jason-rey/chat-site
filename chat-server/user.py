class User():
    def __init__(self, username, addr, port, socket):
        self._name = username
        self._addr = addr
        self._port = port
        self._socket = socket

    @property
    def name(self):
        return self._name

    @property
    def addr(self):
        return self._addr

    @property
    def port(self):
        return self._port

    @property
    def socket(self):
        return self._socket
    
    def send(self, message):
        pass