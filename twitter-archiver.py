import logging
from logging.handlers import TimedRotatingFileHandler

from sqlalchemy import create_engine, Table, Column, String, Integer, MetaData, select

from scrape import scrape_tweets
from settings import USERS, DATABASE_ADDRESS, LOG_LEVEL, LOG_FILE, DB_LOG_LEVEL
from wayback_machine import archive_tweets


logger = logging.getLogger("twitter-archiver")
logger.setLevel(LOG_LEVEL)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch = logging.StreamHandler()
ch.setLevel(LOG_LEVEL)
ch.setFormatter(formatter)
logger.addHandler(ch)
if LOG_FILE:
    fh = TimedRotatingFileHandler(LOG_FILE, when="D", backupCount=2)
    fh.setLevel(LOG_LEVEL)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
logging.getLogger("sqlalchemy.engine").setLevel(DB_LOG_LEVEL)


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
