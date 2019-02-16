import threading
import time
from time import sleep
import logging
from logging.config import fileConfig
from os import path

from processors.parsing import analyse_post

log_file_path = path.join(path.dirname(path.abspath(__file__)), 'logging_config.ini')
logging.config.fileConfig(log_file_path)
logger = logging.getLogger(__name__)

import tweepy

from DB.utility import check_in_db_twitter
from api.api import run
from authentication.auth import get_api_handler
from constants.rilievo import twitter_pages, facebook_pages
from facebook.run import go
from processors.process_tweets import process_source_and_replies


def twitter_go(page):
    count = 0
    api = get_api_handler()

    replies = []

    for source_twit in tweepy.Cursor(api.user_timeline, screen_name=page, timeout=9999999999,
                                     tweet_mode='extended').items():
        if hasattr(source_twit, 'retweeted_status'):
            continue
        if not check_in_db_twitter(source_twit, page):
            continue

        count +=1
        if count == 3:
            logger.info("Twitter changing page")
            break
        try:
            for tweet in tweepy.Cursor(api.search, q='to:%s' % page, since_id=source_twit.id,
                                       result_type='recent',
                                       timeout=99999999999, tweet_mode='extended').items():
                if hasattr(tweet, 'in_reply_to_status_id_str'):
                    if tweet.in_reply_to_status_id_str == source_twit.id_str:
                        replies.append(tweet)
                if len(replies) % 50 == 0 and replies:
                    logger.info("Twitter: " + str(len(replies)))
        except Exception as e:
            logger.info("Exception " + str(e) + " Twitter fetching comments")
            if not replies:
                raise e
        if not replies:
            logger.info("Unable to fetch comments Twitter returning")
            return
        process_source_and_replies(source_twit, replies, page)
        replies.clear()


def start_facebook():
    index = 0
    while True:

        try:
            index = (index + 1) % len(facebook_pages)
            page = facebook_pages[index]
            logger.info("Analysing facebook Page: " + str(page) + "\n")
            go(page)
            logger.info("Calling post analisi")
            analyse_post()
            logger.info("Post Analisi done")
            logger.info("Facebook sleeping per 45 mins")

            sleep(60 * 15)
        except Exception as e:
            logger.error("Got Error Facebook back here in main loop pages")
            logger.error(e)
            sleep(60 * 60)

if __name__ == "__main__":
    th = threading.Thread(target=run)
    th.start()
    facth = threading.Thread(target=start_facebook)
    facth.start()
    index = 0
    while True:
        try:
            index = (index +1)%len(twitter_pages)
            page = twitter_pages[index]
            logger.info("Analysing Twitter Page: " + str(page) + "\n")
            twitter_go(page)
        except Exception as e:
            logger.error(e)
            sleep(60 * 5)

