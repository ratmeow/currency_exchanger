from .utils import setup_package_logger
from .settings import AppSettings

settings = AppSettings()

if not settings.TEST_MODE:
    setup_package_logger()
