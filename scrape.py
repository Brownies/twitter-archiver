import time
import re
from settings import BROWSER_WIDTH, BROWSER_HEIGHT, OPTIONS
from selenium.webdriver import Firefox
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


def scrape_tweets(user):
    with Firefox(options=OPTIONS) as driver:
        driver.set_window_size(BROWSER_WIDTH, BROWSER_HEIGHT)
        driver.get("https://twitter.com/" + user)
        xpath = "//a[contains(@href, \"/" + user + "/status/\"" + ")]"
        WebDriverWait(driver, 5).until(lambda d: d.find_element_by_xpath(xpath))
        seen_tweets = []
        new_tweets = []
        p = re.compile(user + "/status/[0-9]+$")
        current_scroll = 0
        max_scroll = 1

        # Scroll to bottom, scraping tweets along the way because twitter removes them from the DOM as you scroll
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
        return new_tweets
