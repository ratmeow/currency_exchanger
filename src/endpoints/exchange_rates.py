from fastapi import APIRouter, Form, Query, HTTPException
from typing import Annotated
from src.services import ExchangeRateService
from src.utils import DatabaseNotFoundError
from src.schemas import AddExchangeRateRequest, GetExchangeRateResponse, CalculateExchangeRequest
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/exchangeRates",
                   tags=["exchangeRates"])


@router.post("", status_code=201)
async def add_exchange_rate_api(exchange_rate: AddExchangeRateRequest) -> GetExchangeRateResponse:
    exchange = ExchangeRateService.add_exchange_service(exchange_data=exchange_rate)
    return exchange


@router.get("/all", status_code=200)
async def get_all_exchange_rates_api() -> list[GetExchangeRateResponse]:
    exchanges = ExchangeRateService.get_exchanges_service()
    return exchanges


@router.get("/{base_target_code}", status_code=200)
async def get_exchange_api(base_target_code: str) -> GetExchangeRateResponse:
    base_code, target_code = base_target_code[:3], base_target_code[3:]
    try:
        exchange = ExchangeRateService.get_exchange_service(base_code=base_code,
                                                            target_code=target_code)
    except DatabaseNotFoundError:
        raise HTTPException(status_code=404,
                            detail=f"Exchange Rate for this pair Not Found")

    return exchange


@router.patch("/{base_target_code}", status_code=200)
async def update_exchange_api(base_target_code: str, rate: float = Form(...)) -> GetExchangeRateResponse:
    base_code, target_code = base_target_code[:3], base_target_code[3:]
    exchange = ExchangeRateService.update_exchange_service(base_code=base_code,
                                                           target_code=target_code,
                                                           rate=rate)

    return exchange


@router.get("", status_code=200)
async def calculate_exchange_api(exchange_data: Annotated[CalculateExchangeRequest, Query()]):
    return ExchangeRateService.calculate_exchange_service(exchange_data=exchange_data)
