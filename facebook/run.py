import logging
logger = logging.getLogger(__name__)
import datetime
from DB.utility import check_in_db_facebook
from facebook.facebook_access import graph_api_version, access_token
import requests
from dateutil import parser

from facebook.process import process


def get_summary(post_id):
    url = 'https://graph.facebook.com/{}/{}/?fields=shares,likes.summary(true),comments.summary(true)'. \
        format(graph_api_version, post_id)
    r = requests.get(url, params={'access_token': access_token})
    data = r.json()

    if 'error' in data:
        print("got limit summary")
        raise Exception('Limit')

    n_shares = data['shares']['count']
    n_comments = data['comments']['summary']['total_count']
    n_likes = data['likes']['summary']['total_count']
    return n_shares, n_comments, n_likes

"""
Analyse page timeline
"""
def go(page):
    url = 'https://graph.facebook.com/{}/{}/posts'.format(graph_api_version, page)
    r = requests.get(url, params={'access_token': access_token})
    while True:
        data = r.json()
        if 'error' in data:
            logger.warning("Got facebook limit when asking posts (before comments)")
            raise Exception("Limit")

        for d in data['data']:
            if 'message' not in d:
                continue
            created_at = parser.parse(d['created_time']).replace(tzinfo=None)
            delta = datetime.datetime.today() - created_at
            delta_hours = delta.total_seconds() / (60*60)
            if delta_hours < 5:
                #logger.info("Skipping message, as it is too fresh")
                continue
            if not check_in_db_facebook(d['id'], page):
                #logger.info("Skipping Facebook post as already parsed")
                continue
            # Get High level summary
            n_shares, n_comments, n_likes = get_summary(d['id'])

            # Process and store
            process(d['id'], d['created_time'], d['message'], page, n_shares, n_comments, n_likes)

            # Quit after 1 post
            return

        # check if there are more post
        if 'paging' in data and 'next' in data['paging']:
            r = requests.get(data['paging']['next'])
        else:
            break