from fastapi import APIRouter
import hashlib
from fastapi import FastAPI, Request, HTTPException
from config import PRODAMUS_KEY
import hmac

api_router = APIRouter()

SECRET_KEY=PRODAMUS_KEY


@api_router.get("/pulse")
async def root():
    return {"status": "OK"}


async def verify_signature(
    data: list[tuple[str, str]],
    secret_key: str,
    received_sign: str,
) -> bool:

    sorted_items = sorted(data, key=lambda x: x[0])

    sign_string = "".join(str(value) for _, value in sorted_items)

    calculated_sign = hmac.new(
        secret_key.encode("utf-8"),
        sign_string.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()

    return hmac.compare_digest(calculated_sign, received_sign)


@api_router.post("/success-payment-webhook")
async def webhook_handler(request: Request):
    print("Поймал вебхук от Продамуса")

    form = await request.form()
    data = list(form.multi_items())

    received_signature = request.headers.get("Sign")

    if not data:
        print("ошибка 1")
        raise HTTPException(status_code=400, detail="POST body empty")

    if not received_signature:
        print("ошибка 2")
        raise HTTPException(status_code=400, detail="Signature not found in headers")

    is_valid = verify_signature(data, SECRET_KEY, received_signature)

    if not is_valid:
        print("ошибка 3")
        raise HTTPException(status_code=400, detail="Invalid signature")

    print("Подпись совпадает")

    data_dict = dict(data)

    order_id = data_dict.get("order_id")

    if not order_id:
        print("ошибка 4")
        raise HTTPException(status_code=400, detail="order_id missing")

    return {"status": "success"}


