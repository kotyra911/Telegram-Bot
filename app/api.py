from fastapi import APIRouter
import hashlib
from fastapi import FastAPI, Request, HTTPException
from config import PRODAMUS_KEY

api_router = APIRouter()

SECRET_KEY=PRODAMUS_KEY


@api_router.get("/pulse")
async def root():
    return {"status": "OK"}


@api_router.post("/success-payment-webhook")
async def webhook_handler(request: Request):
    print("Поймал вебхук от продамуса")
    
    form = await request.form()
    data = dict(form)

    received_signature = data.pop("signature", None)

    if not received_signature:
        raise HTTPException(status_code=400, detail="No signature")

    # Сортируем параметры
    sorted_items = sorted(data.items())

    # Формируем строку
    sign_string = "".join(str(value) for _, value in sorted_items)
    sign_string += SECRET_KEY

    # Считаем хеш
    calculated_signature = hashlib.sha256(
        sign_string.encode()
    ).hexdigest()

    if calculated_signature != received_signature:
        raise HTTPException(status_code=400, detail="Invalid signature")

    return {"status": "OK"}




