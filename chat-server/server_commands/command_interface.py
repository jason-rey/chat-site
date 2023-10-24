from utils.response import Response

class CommandInterface():
    async def execute(self, **kwargs) -> Response:
        pass
    
    async def create_response(self, status:str="", type:str="", data:dict[str, str|dict]={}) -> Response:
        return Response(status, type, data)

