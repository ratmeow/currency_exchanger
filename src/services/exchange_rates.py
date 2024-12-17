import logging

from src.dao import db_service
from src.schemas import (
    AddExchangeRateRequest,
    CalculateExchangeRequest,
    CalculateExchangeResponse,
    Currency,
    ExchangeRate,
    GetExchangeRateResponse,
)
from src.utils import DatabaseInternalError, DatabaseNotFoundError

logger = logging.getLogger(__name__)


class ExchangeRateService:
    @classmethod
    def get_exchange_service(
        cls, base_code: str, target_code: str
    ) -> GetExchangeRateResponse:
        base_currency, target_currency = cls._get_currency_pair_by_codes(
            base_code=base_code, target_code=target_code
        )

        db_row = db_service.get_exchange(
            base_id=base_currency.id, target_id=target_currency.id
        )

        if len(db_row) == 0:
            raise DatabaseNotFoundError(
                message=f"ExchangeRate [{base_code + target_code}] Not Found"
            )

        exchange = ExchangeRate(**db_row)
        exchange_response = GetExchangeRateResponse(
            id=exchange.id,
            base_currency=base_currency,
            target_currency=target_currency,
            rate=exchange.rate,
        )
        return exchange_response

    @classmethod
    def get_all_exchanges_service(cls) -> list[GetExchangeRateResponse]:
        try:
            db_rows = db_service.get_exchanges()

            if len(db_rows) == 0:
                return []

            raw_exchanges = [ExchangeRate(**row) for row in db_rows]
            exchanges_currencies = [
                cls._get_currency_pair_by_ids(
                    base_id=ex.base_currency_id, target_id=ex.target_currency_id
                )
                for ex in raw_exchanges
            ]
            exchanges = [
                GetExchangeRateResponse(
                    id=ex.id,
                    base_currency=currencies[0],
                    target_currency=currencies[1],
                    rate=ex.rate,
                )
                for ex, currencies in zip(raw_exchanges, exchanges_currencies)
            ]
            return exchanges
        except DatabaseNotFoundError as e:
            logger.error(e.message)
            raise DatabaseInternalError

    @classmethod
    def add_exchange_service(
        cls, exchange_data: AddExchangeRateRequest
    ) -> GetExchangeRateResponse:
        base_currency, target_currency = cls._get_currency_pair_by_codes(
            base_code=exchange_data.base_currency_code,
            target_code=exchange_data.target_currency_code,
        )

        exchange_to_db = ExchangeRate(
            base_currency_id=base_currency.id,
            target_currency_id=target_currency.id,
            rate=exchange_data.rate,
        )

        inserted_exchange = ExchangeRate(
            **db_service.add_exchange(exchange=exchange_to_db.dict(exclude_none=True))
        )

        exchange = GetExchangeRateResponse(
            id=inserted_exchange.id,
            base_currency=base_currency,
            target_currency=target_currency,
            rate=inserted_exchange.rate,
        )
        return exchange

    @classmethod
    def update_exchange_service(
        cls, base_code: str, target_code: str, rate: float
    ) -> GetExchangeRateResponse:
        base_currency, target_currency = cls._get_currency_pair_by_codes(
            base_code=base_code, target_code=target_code
        )

        db_row = db_service.update_exchange(
            base_id=base_currency.id, target_id=target_currency.id, rate=rate
        )

        if len(db_row) == 0:
            raise DatabaseNotFoundError(
                message=f"Exchange [{base_code + target_code}] doesn't exist"
            )

        raw_exchange = ExchangeRate(**db_row)
        exchange = GetExchangeRateResponse(
            id=raw_exchange.id,
            base_currency=base_currency,
            target_currency=target_currency,
            rate=raw_exchange.rate,
        )
        return exchange

    @classmethod
    def calculate_exchange_service(
        cls, exchange_data: CalculateExchangeRequest
    ) -> CalculateExchangeResponse:
        converted = cls._attempt_conversion(
            base_code=exchange_data.base_code,
            target_code=exchange_data.target_code,
            amount=exchange_data.amount,
        )
        if converted:
            return converted

        converted = cls._attempt_conversion(
            base_code=exchange_data.target_code,
            target_code=exchange_data.base_code,
            amount=exchange_data.amount,
            invert_rate=True,
        )
        if converted:
            return converted

        return cls._convert_via_usd(
            base_code=exchange_data.target_code,
            target_code=exchange_data.base_code,
            amount=exchange_data.amount,
        )

    @classmethod
    def _attempt_conversion(
        cls, base_code: str, target_code: str, amount: float, invert_rate: bool = False
    ):
        try:
            exchange = cls.get_exchange_service(
                base_code=base_code, target_code=target_code
            )

            rate = 1 / exchange.rate if invert_rate else exchange.rate

            return CalculateExchangeResponse(
                base_currency=exchange.base_currency,
                target_currency=exchange.target_currency,
                rate=exchange.rate,
                amount=amount,
                converted_amount=rate * amount,
            )

        except DatabaseNotFoundError as e:
            logger.warning(e.message)
            return None

    @classmethod
    def _convert_via_usd(cls, base_code: str, target_code: str, amount: float):
        try:
            usd_from = cls.get_exchange_service(base_code="USD", target_code=base_code)
            usd_to = cls.get_exchange_service(base_code="USD", target_code=target_code)

            return CalculateExchangeResponse(
                base_currency=usd_from.target_currency,
                target_currency=usd_to.target_currency,
                rate=usd_from.rate * usd_to.rate,
                amount=amount,
                converted_amount=(usd_from.rate * usd_to.rate) * amount,
            )

        except DatabaseNotFoundError as e:
            logger.warning(e.message)
            raise DatabaseNotFoundError(
                f"It is impossible to convert[{base_code + target_code}]: "
                f"there is no exchange rate or dollar equivalent"
            )

    @classmethod
    def _get_currency_pair_by_codes(
        cls, base_code: str, target_code: str
    ) -> tuple[Currency, Currency]:
        base_currency_data = db_service.get_currency_by_code(code=base_code)
        target_currency_data = db_service.get_currency_by_code(code=target_code)

        if len(base_currency_data) == 0:
            raise DatabaseNotFoundError(message=f"Currency [{base_code}] Not Found")

        if len(target_currency_data) == 0:
            raise DatabaseNotFoundError(message=f"Currency [{target_code}] Not Found")

        base_currency = Currency(**base_currency_data)
        target_currency = Currency(**target_currency_data)

        return base_currency, target_currency

    @classmethod
    def _get_currency_pair_by_ids(
        cls, base_id: int, target_id: int
    ) -> tuple[Currency, Currency]:
        try:
            base_currency_data = db_service.get_currency_by_id(id_=base_id)
            target_currency_data = db_service.get_currency_by_id(id_=target_id)

            if len(base_currency_data) == 0:
                raise DatabaseNotFoundError(message=f"Currency [{base_id}] Not Found")

            if len(target_currency_data) == 0:
                raise DatabaseNotFoundError(message=f"Currency [{target_id}] Not Found")

            base_currency = Currency(**base_currency_data)
            target_currency = Currency(**target_currency_data)

            return base_currency, target_currency
        except DatabaseInternalError as e:
            raise e
