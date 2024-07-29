from typing import Any

from fastapi import APIRouter

QRrouter = APIRouter()

@QRrouter.get('/qrcode')
async def get_qr()->Any:
    return ...