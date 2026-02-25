from typing import Optional, Any
import json
from fastapi import APIRouter
from config import PRODAMUS_KEY
import logging
from fastapi import Request, Header, HTTPException
import hmac
import hashlib


logger = logging.getLogger(__name__)

api_router = APIRouter()

SECRET_KEY=PRODAMUS_KEY


@api_router.get("/pulse")
async def root():
    return {"status": "OK"}


async def sort_dict(obj: Any) -> Any:
    if isinstance(obj, dict):
        return {k: await sort_dict(obj[k]) for k in sorted(obj)}
    elif isinstance(obj, list):
        return [await sort_dict(i) for i in obj]
    return obj


async def build_signature_from_form(data: dict, secret_key: str) -> str:
    # сортируем рекурсивно
    sorted_payload = await sort_dict(data)

    # сериализация без пробелов
    json_string = json.dumps(
        sorted_payload,
        separators=(",", ":"),
        ensure_ascii=False
    )

    # экранируем /
    json_string = json_string.replace("/", "\\/")

    return hmac.new(
        secret_key.encode(),
        json_string.encode(),
        hashlib.sha256
    ).hexdigest()


@api_router.post("/success-payment-webhook")
async def webhook_handler(
    request: Request,
    sign: Optional[str] = Header(None)
):
    if not sign:
        raise HTTPException(status_code=400, detail="Missing signature")

    # читаем как form-data
    form = await request.form()
    data = dict(form)

    # Строим подпись
    calculated_signature = await build_signature_from_form(data, SECRET_KEY)

    print(calculated_signature)
    print(sign)

    if not hmac.compare_digest(calculated_signature, sign):
        raise HTTPException(status_code=400, detail="Invalid signature")

    print("Webhook verified:", data)

    return {"status": "ok"}



@api_router.post("/debug")
async def webhook_handler(request: Request):
    body = await request.body()
    headers = dict(request.headers)

    logger.info(f"HEADERS: {headers}")
    logger.info(f"RAW BODY: {body}")
    logger.info(f"BODY AS TEXT: {body.decode('utf-8', errors='ignore')}")

    return {"status": "debug"}




