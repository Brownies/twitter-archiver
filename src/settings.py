import logging

from selenium.webdriver.firefox.options import Options


USERS = [
    "jack",
    "michaelmontano",
    "nedsegal"
]
DATABASE_ADDRESS = "sqlite:///db/twitter-archiver.db"
LOG_FILE = "logs/twitter-archiver.log"  # Leave empty to not log to a file
_HEADLESS = True
LOG_LEVEL = logging.INFO
DB_LOG_LEVEL = logging.WARN


BROWSER_WIDTH = 1920
BROWSER_HEIGHT = 1080
OPTIONS = Options()
OPTIONS.headless = _HEADLESS
