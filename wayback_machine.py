import logging
import time

from requests import get
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import Firefox
from selenium.webdriver.support.ui import WebDriverWait

from settings import OPTIONS, LOG_LEVEL, LOG_FILE

logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch = logging.StreamHandler()
ch.setLevel(LOG_LEVEL)
ch.setFormatter(formatter)
logger.addHandler(ch)
if LOG_FILE:
    fh = logging.FileHandler(LOG_FILE)
    fh.setLevel(LOG_LEVEL)
    fh.setFormatter(formatter)
    logger.addHandler(fh)


def archive_tweets(user, tweets):
    logger.info("Archiving %d tweets by %s (Wayback Machine, web.archive.org)" % (len(tweets), user))
    successfully_archived = []
    already_archived = []
    failed = []
    input_id = "web-save-url-input"
    save_button_xpath = "//input[contains(@class, \"web-save-button\") and @type=\"submit\"]"
    done_xpath = "//span[contains(@class, \"label-success\")]"
    with Firefox(options=OPTIONS) as driver:
        for tweet in tweets:
            time.sleep(1)
            r = get("https://archive.org/wayback/available?url=https://twitter.com/" + user + "/status/" + str(tweet))
            if r.json()['archived_snapshots']:
                already_archived.append(tweet)
                logger.debug("Tweet %d already archived" % tweet)
            else:
                try:
                    driver.get("https://web.archive.org/save")
                    WebDriverWait(driver, 5).until(lambda d: d.find_element_by_id(input_id))
                    WebDriverWait(driver, 5).until(lambda d: d.find_element_by_xpath(save_button_xpath))
                    driver.find_element_by_id(input_id).send_keys(
                        "https://twitter.com/" + user + "/status/" + str(tweet)
                    )
                    driver.find_element_by_xpath(save_button_xpath).click()
                    WebDriverWait(driver, 60).until(lambda d: d.find_element_by_xpath(done_xpath))
                    successfully_archived.append(tweet)
                    logger.debug("Successfully archived tweet %d" % tweet)
                except TimeoutException as e:
                    failed.append(tweet)
                    logger.error("Failed to archive tweet %d by %s" % (tweet, user))
                    logger.error(e)

    logger.info("%d tweets failed to archive." % len(failed))
    logger.info("%d tweets already archived." % len(already_archived))
    logger.info("%d tweets successfully archived." % len(successfully_archived))
    return successfully_archived + already_archived
