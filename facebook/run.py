from facebook.facebook_access import graph_api_version, access_token
import requests

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
            print("Got facebook limit")
            raise Exception("Limit")

        for d in data['data']:
            if 'message' not in d:
                continue

            # Get High level summary
            n_shares, n_comments, n_likes = get_summary(d['id'])

            # Process and store
            process(d['id'], d['created_time'], d['message'], page, n_shares, n_comments, n_likes)

        # check if there are more post
        if 'paging' in data and 'next' in data['paging']:
            r = requests.get(data['paging']['next'])
        else:
            break