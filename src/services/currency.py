import logging

from src.dao import db_service
from src.schemas import AddCurrencyRequest, Currency
from src.utils import DatabaseNotFoundError

logger = logging.getLogger(__name__)


class CurrencyService:
    @classmethod
    def get_currencies_service(cls) -> list[Currency]:
        db_rows = db_service.get_currencies()

        if len(db_rows) == 0:
            return []
        currencies = [Currency(**row) for row in db_rows]
        return currencies

    @classmethod
    def add_currency_service(cls, currency: AddCurrencyRequest) -> Currency:
        inserted_row = db_service.add_currency(currency=currency.dict())
        inserted_currency = Currency(**inserted_row)

        return inserted_currency

    @classmethod
    def get_currency_by_name_service(cls, name: str) -> Currency:
        db_row = db_service.get_currency_by_name(name=name)

        if len(db_row) == 0:
            raise DatabaseNotFoundError(message="Currency Not Found")

        currency = Currency(**db_row)
        return currency
