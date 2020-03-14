import time
import re

from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


USERS = ["jack"]
BROWSER_WIDTH = 1920
BROWSER_HEIGHT = 1080
options = Options()
options.headless = True


def scrape_tweets(user):
    driver.get("https://twitter.com/" + user)
    xpath = "//a[contains(@href, \"/" + user + "/status/\"" + ")]"
    WebDriverWait(driver, 5).until(lambda d: d.find_element_by_xpath(xpath))

    # Scroll to bottom of page, scraping tweets along the way because twitter removes them from the DOM as you scroll
    seen_tweets = []
    new_tweets = []
    p = re.compile("(?<=status/)[0-9]+$")
    current_scroll = 0
    max_scroll = 1

    while current_scroll < max_scroll:
        tweets = driver.find_elements_by_xpath(xpath)
        for tweet in tweets:
            n = p.search(tweet.get_attribute("href"))
            if n and (n[0]not in seen_tweets):
                seen_tweets.append(n[0])
                new_tweets.append(n[0])
        ActionChains(driver).send_keys(Keys.PAGE_DOWN, Keys.PAGE_DOWN).perform()
        time.sleep(2)
        current_scroll = driver.execute_script("return window.scrollY;")
        max_scroll = driver.execute_script("return window.scrollMaxY;")
        print("scroll: " + str(current_scroll))
        print("max: " + str(max_scroll))
    return new_tweets


for user in USERS:
    with Firefox(options=options) as driver:
        driver.set_window_size(BROWSER_WIDTH, BROWSER_HEIGHT)
        new_tweets = scrape_tweets(user)
        print(new_tweets)
