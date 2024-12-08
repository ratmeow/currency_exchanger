from src.db import TEST_DB
from src.schemas import AddExchangeRateRequest, ExchangeRate, Currency, ExchangeRateDB, GetExchangeRateResponse
from fastapi import HTTPException
import logging
from src.utils import check_string_is_all_alpha, UniqueError, DatabaseInternalError

logger = logging.getLogger(__name__)


class ExchangeRateService:

    # @classmethod
    # def get_currencies(cls) -> list[Currency]:
    #     try:
    #         db_rows = TEST_DB.get_currencies()
    #     except DatabaseInternalError:
    #         raise HTTPException(status_code=500, detail="Database Error")
    #
    #     currencies = [Currency(**row) for row in db_rows]
    #     return currencies

    @classmethod
    def add_exchange_service(cls, exchange_data: AddExchangeRateRequest) -> GetExchangeRateResponse:
        try:
            base_currency = Currency(**TEST_DB.get_currency_by_code(code=exchange_data.base_currency_code))
            target_currency = Currency(**TEST_DB.get_currency_by_code(code=exchange_data.target_currency_code))

            exchange_to_db = ExchangeRate(base_currency_id=base_currency.id,
                                          target_currency_id=target_currency.id,
                                          rate=exchange_data.rate)

            inserted_exchange = ExchangeRate(**TEST_DB.add_exchange(exchange=exchange_to_db.dict(exclude_none=True)))
        except UniqueError:
            raise HTTPException(status_code=409, detail="A currency pair with this code already exists")
        except DatabaseInternalError:
            raise HTTPException(status_code=500, detail="Database Error")

        inserted_exchange = GetExchangeRateResponse(id=inserted_exchange.id,
                                                    base_currency=base_currency,
                                                    target_currency=target_currency,
                                                    rate=inserted_exchange.rate)
        return inserted_exchange

    # @classmethod
    # def get_currency(cls, name: str) -> Currency:
    #     if not check_string_is_all_alpha(string=name):
    #         raise HTTPException(status_code=400, detail="Currency name has extra characters or digits")
    #     try:
    #         db_row = TEST_DB.get_currency(name=name.upper())
    #     except DatabaseInternalError:
    #         raise HTTPException(status_code=500, detail="Database Error")
    #
    #     if db_row is None:
    #         raise HTTPException(status_code=404, detail="Currency Not Found")
    #
    #     currency = Currency(**db_row)
    #     return currency
