from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from .utils import ServiceValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from .endpoints import currency_router, exchange_router

app = FastAPI()

app.include_router(currency_router)
app.include_router(exchange_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail}
    )


@app.exception_handler(ServiceValidationError)
async def service_validation_exception_handler(request: Request, exc: ServiceValidationError):
    return JSONResponse(
        status_code=400,
        content={"message": exc.message}
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    print(exc)
    messages = []
    for error in exc.errors():
        field = error.get('loc')[-1]
        msg = error.get('msg')
        messages.append(f"Field '{field}' has an error: {msg}")

    return JSONResponse(
        status_code=400,
        content={"message": "; ".join(messages)}
    )


@app.get("/")
async def get_root():
    return {"message": "Hello world"}
