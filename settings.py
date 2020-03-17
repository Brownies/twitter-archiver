import logging

from selenium.webdriver.firefox.options import Options


USERS = [
    "jack",
    "michaelmontano",
    "nedsegal"
]
BROWSER_WIDTH = 1920
BROWSER_HEIGHT = 1080
_HEADLESS = False
DATABASE_ADDRESS = "sqlite:///twitter-archiver.db"
LOG_LEVEL = logging.DEBUG
LOG_FILE = "logs/twitter-archiver.log"  # Leave empty to not log to a file


OPTIONS = Options()
OPTIONS.headless = _HEADLESS
