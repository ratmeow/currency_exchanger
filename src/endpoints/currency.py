import logging
from typing import Annotated

from fastapi import APIRouter, Form, HTTPException

from src.schemas import AddCurrencyRequest, Currency
from src.services import CurrencyService
from src.utils import (
    DatabaseInternalError,
    DatabaseNotFoundError,
    FieldValidator,
    ServiceValidationError,
    UniqueError,
)

logger = logging.getLogger(__name__)

router = APIRouter(tags=["currency"])


@router.get("/currencies", status_code=200)
async def get_currencies_api() -> list[Currency]:
    try:
        currencies = CurrencyService.get_currencies_service()
        return currencies
    except DatabaseInternalError as e:
        raise HTTPException(status_code=500, detail=e.message)


@router.get("/currency/{name}", status_code=200)
async def get_currency_by_name_api(name: str) -> Currency:
    try:
        FieldValidator.check_field_only_letters(value=name, field_name="Currency name")
        currency = CurrencyService.get_currency_by_name_service(name=name)
        return currency
    except ServiceValidationError as e:
        raise HTTPException(status_code=400, detail=e.message)
    except DatabaseNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)
    except DatabaseInternalError as e:
        raise HTTPException(status_code=500, detail=e.message)


@router.post("/currencies", status_code=200)
async def add_currency_api(
    currency_data: Annotated[AddCurrencyRequest, Form()],
) -> Currency:
    try:
        currency = CurrencyService.add_currency_service(currency=currency_data)
        return currency
    except UniqueError as e:
        raise HTTPException(status_code=409, detail=e.message)
    except DatabaseInternalError as e:
        raise HTTPException(status_code=500, detail=e.message)
