import json

class Response:
    def __init__(self, statusCode: str, type="", data:dict[str, str|dict]={}):
        self.statusCode = statusCode
        self.type = type
        self.data = data

    def to_json(self) -> str:
        out = {
            "statusCode": self.statusCode,
            "type": self.type,
            "data": self.data
        }

        return json.dumps(out)