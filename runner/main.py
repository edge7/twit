import argparse
import threading
from time import sleep
from typing import List

import tweepy

from api.api import run
from authentication.auth import get_api_handler
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Sentiment analysis")
    parser.add_argument("--page", help="page to get feed from", required=True)
    args = parser.parse_args()
    pages: List[str] = ['luigidimaio', 'matteosalvinimi']
    th = threading.Thread(target=run)
    th.start()
    index = 0
    while True:
        try:
            index = (index +1)%len(pages)
            page = pages[index]
            main(page)
        except Exception as e:
            print(e)
            sleep(60 * 1)
