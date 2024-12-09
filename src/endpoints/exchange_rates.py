from fastapi import APIRouter, Form, Query, HTTPException, Path
from typing import Annotated
from src.services import ExchangeRateService
from src.utils import DatabaseNotFoundError, DatabaseInternalError, UniqueError, ServiceValidationError, ServiceHelper
from src.schemas import AddExchangeRateRequest, GetExchangeRateResponse, CalculateExchangeRequest
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/exchangeRates",
                   tags=["exchangeRates"])


@router.post("", status_code=201)
async def add_exchange_api(exchange_rate: AddExchangeRateRequest) -> GetExchangeRateResponse:
    try:
        exchange = ExchangeRateService.add_exchange_service(exchange_data=exchange_rate)
    except DatabaseNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)
    except UniqueError as e:
        raise HTTPException(status_code=409, detail=e.message)
    except DatabaseInternalError as e:
        raise HTTPException(status_code=500, detail=e.message)
    return exchange


@router.get("/all", status_code=200)
async def get_all_exchanges_api() -> list[GetExchangeRateResponse]:
    try:
        exchanges = ExchangeRateService.get_all_exchanges_service()
    except DatabaseInternalError as e:
        raise HTTPException(status_code=500, detail=e.message)
    return exchanges


@router.get("/{base_target_code}", status_code=200)
async def get_exchange_api(base_target_code: Annotated[str, Path()]) -> GetExchangeRateResponse:
    try:
        ServiceHelper.check_combined_code(value=base_target_code)

        base_target_code = base_target_code.upper()
        base_code, target_code = base_target_code[:3], base_target_code[3:]

        exchange = ExchangeRateService.get_exchange_service(base_code=base_code,
                                                            target_code=target_code)
        return exchange
    except ServiceValidationError as e:
        raise HTTPException(status_code=400, detail=e.message)
    except DatabaseNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)
    except DatabaseInternalError as e:
        raise HTTPException(status_code=500, detail=e.message)


@router.patch("/{base_target_code}", status_code=200)
async def update_exchange_api(base_target_code: Annotated[str, Path()],
                              rate: float = Form()) -> GetExchangeRateResponse:
    try:
        ServiceHelper.check_combined_code(value=base_target_code)
        ServiceHelper.check_rate(value=rate)

        base_target_code = base_target_code.upper()
        base_code, target_code = base_target_code[:3], base_target_code[3:]

        exchange = ExchangeRateService.update_exchange_service(base_code=base_code,
                                                               target_code=target_code,
                                                               rate=rate)

        return exchange
    except ServiceValidationError as e:
        raise HTTPException(status_code=400, detail=e.message)
    except DatabaseNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)
    except DatabaseInternalError as e:
        raise HTTPException(status_code=500, detail=e.message)


@router.get("", status_code=200)
async def calculate_exchange_api(exchange_data: Annotated[CalculateExchangeRequest, Query()]):
    try:
        return ExchangeRateService.calculate_exchange_service(exchange_data=exchange_data)
    except DatabaseNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)
    except DatabaseInternalError as e:
        raise HTTPException(status_code=500, detail=e.message)
