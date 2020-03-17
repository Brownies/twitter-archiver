import logging

from sqlalchemy import create_engine, Table, Column, String, Integer, MetaData, select

from scrape import scrape_tweets
from settings import USERS, DATABASE_ADDRESS
from wayback_machine import archive_tweets

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

engine = create_engine(DATABASE_ADDRESS)
metadata = MetaData()
archived_tweets = Table(
    "archived_tweets", metadata,
    Column("tweet", Integer, primary_key=True),
    Column("username", String(20), nullable=False)
)
metadata.create_all(engine)
connection = engine.connect()


for user in USERS:
    result = connection.execute(select([archived_tweets.c.tweet]).where(archived_tweets.c.username == user))
    seen_tweets = [r[0] for r in result]
    new_tweets = scrape_tweets(user, seen_tweets)
    if new_tweets:
        new_tweets = archive_tweets(user, new_tweets)
    if new_tweets:
        connection.execute(archived_tweets.insert(), [{"tweet": tweet, "username": user} for tweet in new_tweets])

connection.close()
