from src.db import TEST_DB
from src.schemas import Currency, AddCurrencyRequest
from fastapi import HTTPException
import logging
from src.utils import check_string_is_all_alpha, UniqueError, DatabaseInternalError

logger = logging.getLogger(__name__)


class CurrencyService:

    @classmethod
    def get_currencies_service(cls) -> list[Currency]:
        try:
            db_rows = TEST_DB.get_currencies()
        except DatabaseInternalError:
            raise HTTPException(status_code=500, detail="Database Error")

        if len(db_rows) == 0:
            return []
        currencies = [Currency(**row) for row in db_rows]
        return currencies

    @classmethod
    def add_currency_service(cls, currency: AddCurrencyRequest) -> Currency:
        try:
            inserted_row = TEST_DB.add_currency(currency=currency.dict())
        except UniqueError:
            raise HTTPException(status_code=409, detail="Currency with this code already exists")
        except DatabaseInternalError:
            raise HTTPException(status_code=500, detail="Database Error")

        inserted_currency = Currency(**inserted_row)
        return inserted_currency

    @classmethod
    def get_currency_by_name_service(cls, name: str) -> Currency:
        if not check_string_is_all_alpha(string=name):
            raise HTTPException(status_code=400, detail="Currency name has extra characters or digits")
        try:
            db_row = TEST_DB.get_currency_by_name(name=name)
        except DatabaseInternalError:
            raise HTTPException(status_code=500, detail="Database Error")

        if len(db_row) == 0:
            raise HTTPException(status_code=404, detail="Currency Not Found")

        currency = Currency(**db_row)
        return currency
