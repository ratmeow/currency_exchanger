import sqlite3
import logging

logger = logging.getLogger(__name__)

DB_NAME = "database.db"


def init_db():
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()

            cursor.execute("""PRAGMA foreign_keys = ON;""")

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS currencies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code VARCHAR,
            full_name VARCHAR,
            sign VARCHAR);""")

            cursor.execute("""CREATE UNIQUE INDEX IF NOT EXISTS code_idx on currencies(code);""")

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS exchange_rates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            base_currency_id INTEGER,
            target_currency_id INTEGER,
            rate DECIMAL(6),
            FOREIGN KEY(base_currency_id) REFERENCES currencies(id),
            FOREIGN KEY(target_currency_id) REFERENCES currencies(id)
            );""")

            cursor.execute(
                """CREATE UNIQUE INDEX IF NOT EXISTS base_currency_idx on exchange_rates(base_currency_id);""")
            cursor.execute(
                """CREATE UNIQUE INDEX IF NOT EXISTS target_currency_idx on exchange_rates(target_currency_id);""")

            conn.commit()
    except Exception as e:
        logger.error(msg=f"Error while initializing database: {e}")

init_db()
