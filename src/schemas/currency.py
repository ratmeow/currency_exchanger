from pydantic import BaseModel, field_validator, Field, ConfigDict
from src.utils import check_string_is_all_alpha
from fastapi import HTTPException


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
    def check_name(cls, value):
        if not check_string_is_all_alpha(string=value):
            raise HTTPException(status_code=400, detail="Currency name has extra characters or digits")
        return value

    @field_validator("code")
    def check_code(cls, value: str) -> str:
        return value.upper()
