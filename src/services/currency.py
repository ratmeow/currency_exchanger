from src.db import TEST_DB
from src.schemas import Currency, AddCurrencyRequest
import logging
from src.utils import check_string_is_all_alpha, ServiceValidationError, DatabaseNotFoundError

logger = logging.getLogger(__name__)


class CurrencyService:

    @classmethod
    def get_currencies_service(cls) -> list[Currency]:
        db_rows = TEST_DB.get_currencies()

        if len(db_rows) == 0:
            return []
        currencies = [Currency(**row) for row in db_rows]
        return currencies

    @classmethod
    def add_currency_service(cls, currency: AddCurrencyRequest) -> Currency:
        inserted_row = TEST_DB.add_currency(currency=currency.dict())
        inserted_currency = Currency(**inserted_row)

        return inserted_currency

    @classmethod
    def get_currency_by_name_service(cls, name: str) -> Currency:
        if not check_string_is_all_alpha(string=name):
            raise ServiceValidationError(message="Currency name has extra characters or digits")
        db_row = TEST_DB.get_currency_by_name(name=name)

        if len(db_row) == 0:
            raise DatabaseNotFoundError(message="Currency Not Found")

        currency = Currency(**db_row)
        return currency
