from fastapi import FastAPI
from .endpoints import currency_router, exchange_router

app = FastAPI()

app.include_router(currency_router)
app.include_router(exchange_router)


@app.get("/")
async def get_root():
    return {"message": "Hello world"}
