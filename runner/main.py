import argparse
import sys
import threading
from time import sleep

import tweepy

from api.api import run
from authentication.auth import get_api_handler
from processors.process_tweets import process_source_and_replies


def main(page):
    api = get_api_handler()

    replies = []
    non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

    for source_twit in tweepy.Cursor(api.user_timeline, screen_name=page, timeout=9999999999,
                                     tweet_mode='extended').items():

        for tweet in tweepy.Cursor(api.search, q='to:%s' % page, since_id=source_twit.id,
                                   result_type='recent',
                                   timeout=99999999999, tweet_mode='extended').items():
            if hasattr(tweet, 'in_reply_to_status_id_str'):
                if tweet.in_reply_to_status_id_str == source_twit.id_str:
                    replies.append(tweet)
        process_source_and_replies(source_twit, replies, page)
        #print("Tweet :", source_twit.full_text.translate(non_bmp_map))
        #for elements in replies:
        #    print("Replies :", elements)
        replies.clear()


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Sentiment analysis")
    parser.add_argument("--page", help="page to get feed from", required=True)
    args = parser.parse_args()
    th = threading.Thread(target=run)
    th.start()
    while True:
        try:
            main(args.page)
        except Exception as e:
            sleep(60 * 1)
