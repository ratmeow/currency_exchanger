from pydantic import BaseModel, field_validator, Field, ConfigDict
from src.utils import FieldValidator


class Currency(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: int
    code: str
    full_name: str = Field(alias="name")
    sign: str


class AddCurrencyRequest(BaseModel):
    code: str
    name: str
    sign: str

    @field_validator("name")
    def validate_name(cls, value: str) -> str:
        FieldValidator.check_empty_field(value=value, field_name="name")
        FieldValidator.check_field_only_letters(value=value, field_name="name")
        return value.capitalize()

    @field_validator("code")
    def validate_code(cls, value: str) -> str:
        FieldValidator.check_empty_field(value=value, field_name="code")
        FieldValidator.check_field_only_letters(value=value, field_name="code")
        FieldValidator.check_length_match(value=value, field_name="code", length=3)
        return value.upper()

    @field_validator("sign")
    def validate_sign(cls, value: str) -> str:
        FieldValidator.check_empty_field(value=value, field_name="sign")
        return value
