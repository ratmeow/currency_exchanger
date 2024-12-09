from fastapi import APIRouter, HTTPException
from src.utils import DatabaseNotFoundError, DatabaseInternalError, UniqueError, ServiceValidationError
from src.services import CurrencyService
from src.schemas import AddCurrencyRequest, Currency
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/currency",
                   tags=["currency"])


@router.get("/{name}", status_code=200)
async def get_currency_by_name_api(name: str) -> Currency:
    try:
        currency = CurrencyService.get_currency_by_name_service(name=name)
        return currency
    except ServiceValidationError as e:
        raise HTTPException(status_code=400, detail=e.message)
    except DatabaseNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)
    except DatabaseInternalError as e:
        raise HTTPException(status_code=500, detail=e.message)


@router.post("", status_code=200)
async def add_currency_api(currency_data: AddCurrencyRequest) -> Currency:
    try:
        currency = CurrencyService.add_currency_service(currency=currency_data)
        return currency
    except ServiceValidationError as e:
        raise HTTPException(status_code=400, detail=e.message)
    except UniqueError as e:
        raise HTTPException(status_code=409, detail=e.message)
    except DatabaseInternalError as e:
        raise HTTPException(status_code=500, detail=e.message)


@router.get("/all", status_code=200)
async def get_currencies_api() -> list[Currency]:
    try:
        currencies = CurrencyService.get_currencies_service()
        return currencies
    except DatabaseInternalError as e:
        raise HTTPException(status_code=500, detail=e.message)

