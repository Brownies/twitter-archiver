import logging
import re
import time

from selenium.common.exceptions import WebDriverException
from selenium.webdriver import Firefox
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

from settings import BROWSER_WIDTH, BROWSER_HEIGHT, OPTIONS, LOG_LEVEL, LOG_FILE


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


def scrape_tweets(user, seen_tweets):
    logger.info("Scraping tweets by \"%s\"" % user)
    with Firefox(options=OPTIONS) as driver:
        try:
            driver.set_window_size(BROWSER_WIDTH, BROWSER_HEIGHT)
            driver.get("https://twitter.com/" + user)
            xpath = "//a[contains(@href, \"/" + user + "/status/\"" + ")]"
            WebDriverWait(driver, 5).until(lambda d: d.find_element_by_xpath(xpath))
        except WebDriverException as e:
            logger.error("Could not open page for \"%s\"" % user)
            logger.error(e.msg)
            return []

        new_tweets = []
        p = re.compile("(?<=" + user + "/status/)[0-9]+$")
        current_scroll = 0
        max_scroll = 1
        # Scroll to bottom, scraping tweets along the way because twitter removes them from the DOM as you scroll
        try:
            while current_scroll < max_scroll:
                tweets = driver.find_elements_by_xpath(xpath)
                for tweet in tweets:
                    m = p.search(tweet.get_attribute("href"))
                    if m:
                        n = (int(m[0]))
                        if n not in seen_tweets:
                            seen_tweets.append(n)
                            new_tweets.append(n)
                            logger.debug("Found a new tweet: %d" % n)
                ActionChains(driver).send_keys(Keys.PAGE_DOWN, Keys.PAGE_DOWN).perform()
                time.sleep(2)
                current_scroll = driver.execute_script("return window.scrollY;")
                max_scroll = driver.execute_script("return window.scrollMaxY;")

        except WebDriverException as e:
            logger.error("Error while scraping tweets for \"%s\"" % user)
            logger.error(e.msg)

        logger.info("Found %d new tweets by \"%s\"" % (len(new_tweets), user))
        logger.debug("New tweets: %s" % new_tweets)
        return new_tweets
