from fastapi import Response

from utils.JWT import TokenActions


async def LoginActions(
    response: Response, user_info: dict
) -> dict:
    del user_info['password']
    response.set_cookie(
        key="refresh", 
        value = await TokenActions.generate_jwt(
                payload={'sub': user_info['uuid']}, 
                token_type='refresh'
            ),
        httponly=True
    )
    return {
        'user': user_info, 
        'access' : await TokenActions.generate_jwt(payload = {
            'sub': user_info['uuid'], 'name': user_info['username'], 'email': user_info['email']
        }, token_type='access')
    }