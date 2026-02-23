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
    data: dict,
    secret_key: str,
    received_sign: str,
) -> bool:

    # Сортируем параметры
    sorted_items = sorted(data.items())

    # Формируем строку
    sign_string = "".join(str(value) for _, value in sorted_items)
    sign_string += secret_key

    # Считаем sha256
    calculated_sign = hashlib.sha256(
        sign_string.encode("utf-8")
    ).hexdigest()

    # Безопасное сравнение
    return hmac.compare_digest(calculated_sign, received_sign)


@api_router.post("/success-payment-webhook")
async def webhook_handler(request: Request):
    print("Поймал вебхук от Продамуса")

    # Получаем данные формы
    form = await request.form()
    data = dict(form)

    # Получаем подпись из заголовка
    received_signature = request.headers.get("Sign")

    if not data:
        raise HTTPException(status_code=400, detail="POST body empty")

    if not received_signature:
        raise HTTPException(status_code=400, detail="Signature not found in headers")

    # Проверяем подпись
    is_valid = await verify_signature(data, SECRET_KEY, received_signature)

    if not is_valid:
        raise HTTPException(status_code=400, detail="Invalid signature")

    print("Подпись совпадает")

    order_id = data.get("order_id")

    if not order_id:
        raise HTTPException(status_code=400, detail="order_id missing")

    # 👇 ТУТ должна быть async работа с БД

    return {"status": "success"}



