from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional
from .currency import Currency
from src.utils import ServiceValidationError, ServiceHelper


class ExchangeRate(BaseModel):
    id: Optional[int] = Field(default=None)
    base_currency_id: int
    target_currency_id: int
    rate: float


class AddExchangeRateRequest(BaseModel):
    base_currency_code: str = Field(alias="baseCurrencyCode")
    target_currency_code: str = Field(alias="targetCurrencyCode")
    rate: float

    @field_validator("base_currency_code", "target_currency_code")
    def check_code(cls, value: str) -> str:
        if len(value) != 3:
            raise ServiceValidationError(message=f"Currency code [{value}] must be 3 characters long")
        if not ServiceHelper.check_string_is_all_alpha(value=value):
            raise ServiceValidationError(message=f"Currency code [{value}] has extra characters or digits")
        return value.upper()

    @field_validator("rate")
    def check_rate(cls, value: float) -> float:
        ServiceHelper.check_rate(value)
        return value


class GetExchangeRateResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: int
    base_currency: Currency = Field(alias="baseCurrency")
    target_currency: Currency = Field(alias="targetCurrency")
    rate: float


class CalculateExchangeRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    base_code: str = Field(alias="from")
    target_code: str = Field(alias="to")
    amount: float = Field(alias="amount")


class CalculateExchangeResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    base_currency: Currency = Field(alias="baseCurrency")
    target_currency: Currency = Field(alias="targetCurrency")
    rate: float
    amount: float
    converted_amount: float = Field(alias="convertedAmount")
