import sqlite3
import logging
from typing import Optional
from src.utils import UniqueError, DatabaseInternalError

logger = logging.getLogger(__name__)


class DatabaseService:

    def __init__(self, db_name: str):
        self.db_name = db_name

    def __connect(self):
        try:
            connection = sqlite3.connect(self.db_name)
            connection.row_factory = sqlite3.Row
            return connection
        except Exception as e:
            logger.error(e)
            raise

    def get_currencies(self) -> list[dict]:
        with self.__connect() as conn:
            cursor = conn.cursor()

            query = """
            SELECT * FROM currencies"""

            try:
                result = [dict(row) for row in cursor.execute(query).fetchall()]
                return result
            except Exception as e:
                logger.error(e)
                raise

    def add_currency(self, currency: dict) -> dict:
        with self.__connect() as conn:
            cursor = conn.cursor()

            query = f"""
            INSERT INTO currencies (code, full_name, sign) VALUES(?, ?, ?) RETURNING *;"""

            try:
                result = cursor.execute(query, tuple(currency.values())).fetchone()
                conn.commit()
                return dict(result)
            except sqlite3.IntegrityError as e:
                logger.error(e)
                raise UniqueError
            except Exception as e:
                logger.error(e)
                raise DatabaseInternalError

    def get_currency_by_id(self, id_: int) -> dict:
        with self.__connect() as conn:
            cursor = conn.cursor()

            query = f"""
            SELECT * FROM currencies WHERE id = '{id_}';"""

            try:
                result = cursor.execute(query).fetchone()

                if result is None:
                    result = dict()

                return result
            except Exception as e:
                logger.error(e)
                raise DatabaseInternalError

    def get_currency_by_name(self, name: str) -> dict:
        with self.__connect() as conn:
            cursor = conn.cursor()

            query = f"""
            SELECT * FROM currencies WHERE full_name = '{name}';"""

            try:
                result = cursor.execute(query).fetchone()

                if result is None:
                    result = dict()

                return result
            except Exception as e:
                logger.error(e)
                raise DatabaseInternalError

    def get_currency_by_code(self, code: str) -> dict:
        with self.__connect() as conn:
            cursor = conn.cursor()

            query = f"""
            SELECT * FROM currencies WHERE code = '{code}';"""

            try:
                result = cursor.execute(query).fetchone()

                if result is None:
                    result = dict()

                return result
            except Exception as e:
                logger.error(e)
                raise DatabaseInternalError

    def add_exchange(self, exchange: dict) -> dict:
        with self.__connect() as conn:
            cursor = conn.cursor()

            query = f"""
            INSERT INTO exchange_rates (base_currency_id, target_currency_id, rate) VALUES(?, ?, ?) RETURNING *;"""

            try:
                result = cursor.execute(query, tuple(exchange.values())).fetchone()
                conn.commit()
                return dict(result)
            except sqlite3.IntegrityError as e:
                logger.error(e)
                raise UniqueError
            except Exception as e:
                logger.error(e)
                raise DatabaseInternalError

    def get_exchanges(self) -> list[dict]:
        with self.__connect() as conn:
            cursor = conn.cursor()

            query = """
            SELECT * FROM exchange_rates"""

            try:
                result = [dict(row) for row in cursor.execute(query).fetchall()]
                return result
            except Exception as e:
                logger.error(e)
                raise

    def get_exchange(self, base_id: str, target_id: str) -> dict:
        with self.__connect() as conn:
            cursor = conn.cursor()

            query = f"""
            SELECT * FROM exchange_rates 
            WHERE base_currency_id = '{base_id}' AND target_currency_id = '{target_id}';"""

            try:
                result = cursor.execute(query).fetchone()

                if result is None:
                    result = dict()

                return result
            except Exception as e:
                logger.error(e)
                raise DatabaseInternalError

    def update_exchange(self, base_id: str, target_id: str, rate: float) -> dict:
        with self.__connect() as conn:
            cursor = conn.cursor()

            query = f"""
            UPDATE exchange_rates 
            SET rate = {rate}
            WHERE base_currency_id = '{base_id}' AND target_currency_id = '{target_id}'
            RETURNING *;"""

            try:
                result = cursor.execute(query).fetchone()
                conn.commit()
                return dict(result)
            except Exception as e:
                logger.error(e)
                raise DatabaseInternalError


TEST_DB = DatabaseService("database.db")
