from fastapi import APIRouter
from src.services import CurrencyService
from src.schemas import AddCurrencyRequest, Currency
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/currency",
                   tags=["currency"])


@router.get("/{name}", status_code=200)
async def get_currency_by_name_api(name: str) -> Currency:
    currency = CurrencyService.get_currency_by_name_service(name=name)
    return currency


@router.post("", status_code=200)
async def add_currency_api(currency_data: AddCurrencyRequest) -> Currency:
    currency = CurrencyService.add_currency_service(currency=currency_data)
    return currency
