from selenium.webdriver.firefox.options import Options


USERS = [
    "jack",
    "michaelmontano"
    "nedsegal"
]
BROWSER_WIDTH = 1920
BROWSER_HEIGHT = 1080
_HEADLESS = True


OPTIONS = Options()
OPTIONS.headless = _HEADLESS
