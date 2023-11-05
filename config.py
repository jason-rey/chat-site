from dotenv import load_dotenv
import os

load_dotenv()

class Config():
    HOST_IP = os.getenv("host_ip")
    HOST_PORT = os.getenv("PORT")

    AUTH_SERVER_IP = os.getenv("auth_server_ip")