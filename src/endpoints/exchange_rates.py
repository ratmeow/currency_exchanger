import logging
from typing import Annotated

from fastapi import APIRouter, Form, HTTPException, Path, Query

from src.schemas import (
    AddExchangeRateRequest,
    CalculateExchangeRequest,
    CalculateExchangeResponse,
    GetExchangeRateResponse,
)
from src.services import ExchangeRateService
from src.utils import (
    DatabaseInternalError,
    DatabaseNotFoundError,
    FieldValidator,
    ServiceValidationError,
    UniqueError,
    split_and_up_base_target_code,
)

logger = logging.getLogger(__name__)

router = APIRouter(tags=["exchangeRates"])


@router.post("/exchangeRates", status_code=201)
async def add_exchange_api(
    exchange_rate: Annotated[AddExchangeRateRequest, Form()],
) -> GetExchangeRateResponse:
    try:
        exchange = ExchangeRateService.add_exchange_service(exchange_data=exchange_rate)
    except DatabaseNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)
    except UniqueError as e:
        raise HTTPException(status_code=409, detail=e.message)
    except DatabaseInternalError as e:
        raise HTTPException(status_code=500, detail=e.message)
    return exchange


@router.get("/exchangeRates", status_code=200)
async def get_all_exchanges_api() -> list[GetExchangeRateResponse]:
    try:
        exchanges = ExchangeRateService.get_all_exchanges_service()
    except DatabaseInternalError as e:
        raise HTTPException(status_code=500, detail=e.message)
    return exchanges


@router.get("/exchange", status_code=200)
async def calculate_exchange_api(
    exchange_data: Annotated[CalculateExchangeRequest, Query()],
) -> CalculateExchangeResponse:
    try:
        return ExchangeRateService.calculate_exchange_service(
            exchange_data=exchange_data
        )
    except DatabaseNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)
    except DatabaseInternalError as e:
        raise HTTPException(status_code=500, detail=e.message)


@router.get("/exchangeRate/{base_target_code}", status_code=200)
async def get_exchange_api(
    base_target_code: Annotated[str, Path()],
) -> GetExchangeRateResponse:
    try:
        FieldValidator.check_combined_code(value=base_target_code, field_name="code")

        base_code, target_code = split_and_up_base_target_code(
            base_target_code=base_target_code
        )

        exchange = ExchangeRateService.get_exchange_service(
            base_code=base_code, target_code=target_code
        )
        return exchange
    except ServiceValidationError as e:
        raise HTTPException(status_code=400, detail=e.message)
    except DatabaseNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)
    except DatabaseInternalError as e:
        raise HTTPException(status_code=500, detail=e.message)


@router.patch("/exchangeRate/{base_target_code}", status_code=200)
async def update_exchange_api(
    base_target_code: Annotated[str, Path()], rate: float = Form()
) -> GetExchangeRateResponse:
    try:
        FieldValidator.check_combined_code(value=base_target_code, field_name="code")
        FieldValidator.check_field_not_negative(value=rate, field_name="rate")

        base_code, target_code = split_and_up_base_target_code(
            base_target_code=base_target_code
        )

        exchange = ExchangeRateService.update_exchange_service(
            base_code=base_code, target_code=target_code, rate=rate
        )

        return exchange
    except ServiceValidationError as e:
        raise HTTPException(status_code=400, detail=e.message)
    except DatabaseNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)
    except DatabaseInternalError as e:
        raise HTTPException(status_code=500, detail=e.message)
