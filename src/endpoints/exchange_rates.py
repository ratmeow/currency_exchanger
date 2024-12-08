from fastapi import APIRouter
from src.services import ExchangeRateService
from src.schemas import AddExchangeRateRequest, GetExchangeRateResponse
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/exchangeRates",
                   tags=["exchangeRates"])


@router.post("", status_code=201)
async def add_exchange_rate_api(exchange_rate: AddExchangeRateRequest) -> GetExchangeRateResponse:
    exchange = ExchangeRateService.add_exchange_service(exchange_data=exchange_rate)
    return exchange


# @router.post("", status_code=200)
# async def add_currency(currency: AddCurrencyRequest) -> GetCurrencyResponse:
#     response = GetCurrencyResponse(**CurrencyService.add_currency(currency=currency).dict())
#     return response
