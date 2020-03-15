import time

from requests import get
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import Firefox
from selenium.webdriver.support.ui import WebDriverWait

from settings import OPTIONS


def archive_tweets(user, tweets):
    print("Archiving " + str(len(tweets)) + " tweets (archive.org)")
    successfully_archived = []
    input_id = "web-save-url-input"
    save_button_xpath = "//input[contains(@class, \"web-save-button\") and @type=\"submit\"]"
    done_xpath = "//span[contains(@class, \"label-success\")]"
    failed = []
    with Firefox(options=OPTIONS) as driver:
        for tweet in tweets:
            time.sleep(1)
            r = get("https://archive.org/wayback/available?url=https://twitter.com/" + user + "/status/" + str(tweet))
            if r.json()['archived_snapshots']:
                successfully_archived.append(tweet)
            else:
                try:
                    print("opening archive save page")
                    driver.get("https://web.archive.org/save")
                    WebDriverWait(driver, 5).until(lambda d: d.find_element_by_id(input_id))
                    WebDriverWait(driver, 5).until(lambda d: d.find_element_by_xpath(save_button_xpath))
                    driver.find_element_by_id(input_id).send_keys(
                        "https://twitter.com/" + user + "/status/" + str(tweet)
                    )
                    driver.find_element_by_xpath(save_button_xpath).click()
                    WebDriverWait(driver, 60).until(lambda d: d.find_element_by_xpath(done_xpath))
                    successfully_archived.append(tweet)
                except TimeoutException as e:
                    failed.append(tweet)
                    print(e)
    print(str(len(failed)) + " tweets failed to archive.")
    print(str(len(successfully_archived)) + " tweets already archived or added to archive.")
    return successfully_archived
