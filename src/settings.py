from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    TEST_MODE: bool = False
    DB_NAME: str = "database.db"
    SCHEMA_PATH: str = "src/data/schema.sql"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if self.TEST_MODE:
            self.DB_NAME = "test_database.db"
            self.SCHEMA_PATH = "data/test_schema.sql"
