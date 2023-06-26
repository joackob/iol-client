import requests
from dataclasses import dataclass
from os import getenv

URL = "https://api.invertironline.com/token"
HEADER_REQUEST = {"Content-Type": "application/x-www-form-urlencoded"}


# POST /token HTTP/1.1
# Host: api.invertironline.com
# Content-Type: application/x-www-form-urlencoded
# username=MIUSUARIO&password=MICONTRASEÑA&grant_type=password
@dataclass
class Token:
    response: requests.Response | None = None
    user: str = ""
    password: str = ""

    def connect(self):
        self.response = requests.post(
            URL,
            headers=HEADER_REQUEST,
            data={
                "username": self.user,
                "password": self.password,
                "grant_type": "password",
            },
        )
        return self.response.status_code
