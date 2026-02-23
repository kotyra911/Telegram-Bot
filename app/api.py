from fastapi import APIRouter
import hashlib
from fastapi import FastAPI, Request, HTTPException
from config import PRODAMUS_KEY
import hmac
import logging


logger = logging.getLogger(__name__)

api_router = APIRouter()

SECRET_KEY=PRODAMUS_KEY


@api_router.get("/pulse")
async def root():
    return {"status": "OK"}


async def verify_signature(
    body: bytes,
    secret_key: str,
    received_sign: str,
) -> bool:

    calculated_sign = hmac.new(
        secret_key.encode("utf-8"),
        body,
        hashlib.sha256,
    ).hexdigest()

    return hmac.compare_digest(calculated_sign, received_sign)


@api_router.post("/success-payment-webhook")
async def webhook_handler(request: Request):
    print("Поймал вебхук от Продамуса")

    body = await request.body()
    received_signature = request.headers.get("Sign")

    if not body:
        print("Нет тела запроса")
        raise HTTPException(status_code=400, detail="POST body empty")

    if not received_signature:
        print("Не найдена подпись в заголовке")
        raise HTTPException(status_code=400, detail="Signature not found in headers")

    is_valid = await verify_signature(body, SECRET_KEY, received_signature)

    if not is_valid:
        print("Подпись НЕ совпадает")
        raise HTTPException(status_code=400, detail="Invalid signature")

    print("Подпись совпадает")

    return {"status": "success"}




@api_router.post("/debug")
async def webhook_handler(request: Request):
    body = await request.body()
    headers = dict(request.headers)

    logger.info(f"HEADERS: {headers}")
    logger.info(f"RAW BODY: {body}")
    logger.info(f"BODY AS TEXT: {body.decode('utf-8', errors='ignore')}")

    return {"status": "debug"}


