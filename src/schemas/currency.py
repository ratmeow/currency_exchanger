from pydantic import BaseModel, field_validator, Field, ConfigDict
from src.utils import ServiceHelper, ServiceValidationError


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
    def check_name(cls, value: str) -> str:
        if not ServiceHelper.check_string_is_all_alpha(value=value):
            raise ServiceValidationError(message="Currency name has extra characters or digits")
        return value.capitalize()

    @field_validator("code")
    def check_code(cls, value: str) -> str:
        if len(value) != 3:
            raise ServiceValidationError(message=f"Currency code [{value}] must be 3 characters long")
        if not ServiceHelper.check_string_is_all_alpha(value=value):
            raise ServiceValidationError(message=f"Currency code [{value}] has extra characters or digits")
        return value.upper()
