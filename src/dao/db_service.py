import logging
import os
import sqlite3

from src import settings
from src.utils import DatabaseInternalError, UniqueError

logger = logging.getLogger(__name__)


class DatabaseService:
    def __init__(self):
        self.db_name = settings.DB_NAME
        if not os.path.exists(self.db_name) or settings.TEST_MODE:
            self._init_db()

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
                result = [
                    dict(row) if row is not None else dict()
                    for row in cursor.execute(query).fetchall()
                ]
                return result
            except Exception as e:
                logger.error(e)
                raise DatabaseInternalError

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
                raise UniqueError(message="Currency with this code already exist")
            except Exception as e:
                logger.error(e)
                raise DatabaseInternalError

    def get_currency_by_id(self, id_: int) -> dict:
        with self.__connect() as conn:
            cursor = conn.cursor()

            query = f"""
            SELECT * FROM currencies WHERE id = ?;"""

            try:
                result = cursor.execute(query, (id_,)).fetchone()

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
            SELECT * FROM currencies WHERE full_name = ?;"""

            try:
                result = cursor.execute(query, (name, )).fetchone()

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
            SELECT * FROM currencies WHERE code = ?;"""

            try:
                result = cursor.execute(query, (code,)).fetchone()

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
                raise UniqueError(
                    message="A currency pair with this code already exists"
                )
            except Exception as e:
                logger.error(e)
                raise DatabaseInternalError

    def get_exchanges(self) -> list[dict]:
        with self.__connect() as conn:
            cursor = conn.cursor()

            query = """
            SELECT * FROM exchange_rates"""

            try:
                result = [
                    dict(row) if row is not None else dict()
                    for row in cursor.execute(query).fetchall()
                ]
                return result
            except Exception as e:
                logger.error(e)
                raise DatabaseInternalError

    def get_exchange(self, base_id: int, target_id: int) -> dict:
        with self.__connect() as conn:
            cursor = conn.cursor()

            query = f"""
            SELECT * FROM exchange_rates 
            WHERE base_currency_id = ? AND target_currency_id = ?;"""

            try:
                result = cursor.execute(query, (base_id, target_id)).fetchone()
                return dict(result) if result is not None else dict()
            except Exception as e:
                logger.error(e)
                raise DatabaseInternalError

    def update_exchange(self, base_id: int, target_id: int, rate: float) -> dict:
        with self.__connect() as conn:
            cursor = conn.cursor()

            query = f"""
            UPDATE exchange_rates 
            SET rate = ?
            WHERE base_currency_id = ? AND target_currency_id = ?
            RETURNING *;"""

            try:
                result = cursor.execute(query, (rate, base_id, target_id)).fetchone()
                conn.commit()
                return dict(result) if result is not None else dict()
            except Exception as e:
                logger.error(e)
                raise DatabaseInternalError

    def _init_db(self):
        logger.info("Initializing database....")
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()

                with open(settings.SCHEMA_PATH, "r") as f:
                    sql_script = f.read()
                    cursor.executescript(sql_script)

                conn.commit()
        except Exception as e:
            logger.error(msg=f"Error while initializing database: {e}")
