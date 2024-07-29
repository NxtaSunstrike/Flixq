from fastapi import Response


async def logout(response: Response) -> dict:
    response.delete_cookie(key='refresh')
    return {'message': 'Logout successful'}