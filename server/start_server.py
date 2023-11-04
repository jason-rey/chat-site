import asyncio

from chat_server import Server
from config import Config

if __name__ == "__main__":
    server = Server(Config.HOST_IP, Config.HOST_PORT)
    asyncio.run(server.start())