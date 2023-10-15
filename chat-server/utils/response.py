import json

class Response:
    def __init__(self, _statusCode: str, _type="", _data={}):
        self.statusCode = _statusCode
        self.type = _type
        self.data = _data

    def to_json(self):
        out = {
            "statusCode": self.statusCode,
            "type": self.type,
            "data": self.data
        }

        return json.dumps(out)