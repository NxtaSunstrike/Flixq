from utils.JWT import JWT

from StreamPool.app import router

@router.subscriber(stream='CheckJWT')
async def CheckJWT(
    token:str, type: str
):
    return await JWT.check_token(token=token, type=type)