from utils.response import Response

class CommandInterface():
    responseStatusEnum = Response.StatusType
    
    def __init__(self, actionName:str=""):
        self.actionName = actionName

    async def execute(self, **kwargs) -> Response:
        pass
    
    async def create_response(self, status:Response.StatusType, type:str="", data:dict[str, str|dict]={}) -> Response:
        return Response(status, type=type, data=data)

