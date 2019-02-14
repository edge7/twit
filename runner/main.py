import argparse
import threading
from time import sleep
from typing import List

import tweepy

from api.api import run
from authentication.auth import get_api_handler
from constants.rilievo import twitter_pages, facebook_pages
from facebook.run import go
from processors.process_tweets import process_source_and_replies


def main(page):
    api = get_api_handler()

    replies = []

    for source_twit in tweepy.Cursor(api.user_timeline, screen_name=page, timeout=9999999999,
                                     tweet_mode='extended').items():
        if hasattr(source_twit, 'retweeted_status'):
            continue
        for tweet in tweepy.Cursor(api.search, q='to:%s' % page, since_id=source_twit.id,
                                   result_type='recent',
                                   timeout=99999999999, tweet_mode='extended').items():

            if hasattr(tweet, 'in_reply_to_status_id_str'):
                if tweet.in_reply_to_status_id_str == source_twit.id_str:
                    replies.append(tweet)
        process_source_and_replies(source_twit, replies, page)
        replies.clear()


def start_facebook():
    index = 0
    while True:
        try:
            index = (index + 1) % len(facebook_pages)
            page = facebook_pages[index]
            print("\n\n")
            print("Analysing facebook Page: " + str(page))
            print("\n\n")
            go(page)
        except Exception as e:
            print(e)
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
            print("\n\n")
            print("Analysing Twitter Page: " + str(page))
            print("\n\n")
            main(page)
        except Exception as e:
            print(e)
            sleep(60 * 15)

