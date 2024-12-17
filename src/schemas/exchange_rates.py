from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

from src.utils import FieldValidator

from .currency import Currency


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
    def validate_code(cls, value: str) -> str:
        FieldValidator.check_field_only_letters(value=value, field_name="code")
        FieldValidator.check_length_match(value=value, field_name="code", length=3)
        return value.upper()

    @field_validator("rate")
    def validate_rate(cls, value: float) -> float:
        FieldValidator.check_field_not_negative(value=value, field_name="rate")
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

    @field_validator("amount")
    def validate_amount(cls, value: float) -> float:
        FieldValidator.check_field_not_negative(value=value, field_name="amount")
        return value


class CalculateExchangeResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    base_currency: Currency = Field(alias="baseCurrency")
    target_currency: Currency = Field(alias="targetCurrency")
    rate: float
    amount: float
    converted_amount: float = Field(alias="convertedAmount")

    @field_validator("converted_amount")
    def validate_converted_amount(cls, value: float) -> float:
        return round(value, 2)
