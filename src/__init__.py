from .settings import AppSettings
from .utils import setup_package_logger

settings = AppSettings()

if not settings.TEST_MODE:
    setup_package_logger()
