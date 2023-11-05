import json
from enum import Enum

class Response: 
    class StatusType(Enum):
        OK = "ok"
        ERROR = "error"   

    def __init__(self, status: StatusType, type:str="", data:dict[str, str|dict]={}):
        self.status = status
        self.type = type
        self.data = data

    def to_json(self) -> str:
        """
            Response format:
            {
                "statusCode": a StatusType,
                "type": the type of response,
                "data": json containing data
            }
        """
        out = {
            "statusCode": self.status.value,
            "type": self.type,
            "data": self.data
        }

        return json.dumps(out)
    