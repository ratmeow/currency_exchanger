from fastapi import APIRouter
from src.services import CurrencyService
from src.schemas import Currency

router = APIRouter(prefix="/currencies",
                   tags=["currencies"])


@router.get("", status_code=200)
async def get_currencies_api() -> list[Currency]:
    currencies = CurrencyService.get_currencies_service()
    return currencies


