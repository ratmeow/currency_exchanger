from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from .currency import Currency


class ExchangeRate(BaseModel):
    id: Optional[int] = Field(default=None)
    base_currency_id: int
    target_currency_id: int
    rate: float


class ExchangeRateDB(BaseModel):
    base_currency_id: int
    target_currency_id: int
    rate: float


class AddExchangeRateRequest(BaseModel):
    base_currency_code: str = Field(alias="baseCurrencyCode")
    target_currency_code: str = Field(alias="targetCurrencyCode")
    rate: float


class GetExchangeRateResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: int
    base_currency: Currency = Field(alias="baseCurrency")
    target_currency: Currency = Field(alias="targetCurrency")
    rate: float
