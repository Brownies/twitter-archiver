from settings import USERS
from scrape import scrape_tweets
from wayback_machine import archive_tweets


for user in USERS:
    new_tweets = scrape_tweets(user)
    archive_tweets(new_tweets)
