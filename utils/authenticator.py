import requests

from .authenticator_interface import AuthenticatorInterface
from room_logic import User

class Authenticator(AuthenticatorInterface):
    def __init__(self, _ip: str):
        self.ip = _ip

    async def check(self, user: User, givenToken: str) -> bool:
        headers = {
            "username": user.name,
        }

        body = {
            "token": givenToken
        }

        url = f"https://{self.ip}/authenticate-token"
        response = requests.post(
            url=url,
            headers=headers,
            json=body
        )

        if response.status_code != 200:
            print(response.json())
            return False
        
        return True
