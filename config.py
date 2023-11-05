from dotenv import load_dotenv
import os

load_dotenv()

class Config():
    HOST_IP = os.getenv("host_ip")
    HOST_PORT = os.getenv("host_port")

    AUTH_SERVER_IP = os.getenv("auth_server_ip")
    AUTH_SERVER_PORT = os.getenv("auth_server_port")