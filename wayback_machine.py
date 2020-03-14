import time
from requests import get
from selenium.webdriver import Firefox
from selenium.webdriver.support.ui import WebDriverWait
from settings import OPTIONS


def archive_tweets(tweets):
    successfully_archived = []
    input_id = "web-save-url-input"
    save_button_xpath = "//input[contains(@class, \"web-save-button\") and @type=\"submit\"]"
    with Firefox(options=OPTIONS) as driver:
        for tweet in tweets:
            r = get("https://archive.org/wayback/available?url=https://twitter.com/" + tweet)
            if r.json()['archived_snapshots']:
                successfully_archived.append(tweet)
            else:
                driver.get("https://web.archive.org/save")
                WebDriverWait(driver, 5).until(lambda d: d.find_element_by_id(input_id))
                WebDriverWait(driver, 5).until(lambda d: d.find_element_by_xpath(save_button_xpath))
                driver.find_element_by_id(input_id).send_keys("https://twitter.com/" + tweet)
                driver.find_element_by_xpath(save_button_xpath).click()
                time.sleep(20)

    return successfully_archived
