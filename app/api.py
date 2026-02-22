from fastapi import APIRouter

api_router = APIRouter()


@api_router.get("/pulse")
async def root():
    return {"status": "OK"}


@api_router.post("/success-payment-webhook")
async def root():
    print("Поймал вебхук от продамуса")
    return {"status": "OK"}




