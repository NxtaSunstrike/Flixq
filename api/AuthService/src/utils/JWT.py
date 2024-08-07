from fastapi import HTTPException, Depends
import jwt
from datetime import datetime, timedelta
from settings.AuthSettings import JWTSet

from sqlalchemy.ext.asyncio import AsyncSession
from db.Postgres.crud.Requests import Operations

from db.Postgres.Base import get_session


class JWT:
    secret: str = JWTSet.secret.read_text()
    public: str = JWTSet.public.read_text()
    access_exp_min: int = JWTSet.expire_minutes
    access_exp_day:int  = JWTSet.expire_days
    algorithm: str = JWTSet.algorithm
        

    async def generate_jwt(self, payload: dict, token_type: str) -> str:
        payload = payload.copy()
        if token_type == 'refresh':
            exp = datetime.now() + timedelta(days=self.access_exp_day)
        elif token_type == 'access':
            exp = datetime.now() + timedelta(minutes=self.access_exp_min)
        else:
            raise HTTPException(400, 'Invalid token type')
        
        payload.update(
            {'type': token_type, 'exp': exp}
        )
        encoded_jwt = jwt.encode(
            payload=payload,
            key=self.secret,
            algorithm=self.algorithm,
        )
        
        return encoded_jwt
    

    async def decode_jwt(self, encoded_jwt: str | bytes) -> dict:
        try:
            decoded_jwt = jwt.decode(
                jwt=encoded_jwt,
                key=self.public,
                algorithms=[self.algorithm],
            )
        except (jwt.DecodeError, jwt.ExpiredSignatureError):
            return {}
        return decoded_jwt
    

    async def check_token(self, token: str | bytes, type: str) -> dict | HTTPException:
        try:
           decoded = await self.decode_jwt(encoded_jwt=token)
        except jwt.DecodeError:
            raise HTTPException(401, detail='Invalid token')
        if decoded['type'] != type:
            raise HTTPException(401, detail= f'Invalid Token {decoded['type']} expected {type}' )
        return decoded
    
    
    async def Refresh(
            self, token: str | bytes, type: str,  DbSession: AsyncSession = Depends(get_session)
        ) -> dict:
        if (decoded:=await self.check_token(token=token, type=type)):
            user = await Operations.get_item(DbSession=DbSession, item_uuid=decoded['sub'])
            return {
                'access': await self.generate_jwt(
                    payload={
                        'sub': str(user['uuid']),
                        'name': user['username'],
                        'email': user['email'],
                        'uuid': str(user['uuid'])
                    },
                    token_type='access'
                )  
            }
        raise HTTPException(status_code=401, detail='Invalid Token')

TokenActions = JWT()