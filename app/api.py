from typing import Optional

from fastapi import APIRouter
from flet_core.icons import PRINT

from config import PRODAMUS_KEY
import logging
from fastapi import FastAPI, Request, Header, HTTPException
import hmac
import hashlib


logger = logging.getLogger(__name__)

api_router = APIRouter()

SECRET_KEY=PRODAMUS_KEY


@api_router.get("/pulse")
async def root():
    return {"status": "OK"}


@api_router.post("/success-payment-webhook")
async def webhook_handler(request: Request, sign: Optional[str] = Header(None)):
        body = await request.body()

        print(body)


        # Проверяем подпись
        signature = hmac.new(SECRET_KEY.encode(), body, hashlib.sha256).hexdigest()

        print(signature)
        print(sign)

        if signature != sign:
            raise HTTPException(status_code=400, detail="Invalid signature")

        data = await request.json()
        print("Получены данные:", data)
        return {"status": "ok"}




@api_router.post("/debug")
async def webhook_handler(request: Request):
    body = await request.body()
    headers = dict(request.headers)

    logger.info(f"HEADERS: {headers}")
    logger.info(f"RAW BODY: {body}")
    logger.info(f"BODY AS TEXT: {body.decode('utf-8', errors='ignore')}")

    return {"status": "debug"}




