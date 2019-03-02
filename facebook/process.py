from time import sleep
import logging

logger = logging.getLogger(__name__)
import requests
from dateutil import parser

from DB.utility import insertFacebook
from facebook.facebook_access import graph_api_version, access_token
from processors.parsing import tokenize, tokenize_post, get_hashtags
from processors.process_tweets import replace_weird_chars


def get_summary_comment(comment_id, index):
    url = 'https://graph.facebook.com/{}/{}/?fields=likes.summary(true),comments.summary(true)'. \
        format(graph_api_version, comment_id)
    r = requests.get(url, params={'access_token': access_token[index]})
    data = r.json()
    if 'error' in data:
        raise Exception(data['error']['message'])

    try:
        n_comments = data['comments']['summary']['total_count']
        n_likes = data['likes']['summary']['total_count']
    except Exception as e:
        n_comments = 0
        n_likes = 0
    return n_comments, n_likes


def process(id_post, c_time, message, page, n_shares, n_comments, n_likes, index_token):
    c_time = parser.parse(c_time)


    def get_delay(n):
        return 0.3

    message = replace_weird_chars(message)
    url = 'https://graph.facebook.com/{}/{}/comments?summary=1&filter=toplevel'.format(graph_api_version, id_post)
    delay = get_delay(n_comments)
    #logger.info("#Comments: " + str(n_comments))
    #logger.info("Delay is: "+ str(delay))
    comments = []

    best_comments = []
    r = requests.get(url, params={'access_token': access_token[index_token]})
    j = 0
    while True:
        data = r.json()

        # catch errors returned by the Graph API
        if 'error' in data:
            print("Limit error when asking comments")
            if len(comments) > 1000:
                logger.warning("Skipping error as I have enough comments")
                break
            raise Exception(data['error']['message'])

        # append the text of each comment into the comments list
        for comment in data['data']:
            text = comment['message'].replace('\n', ' ')
            text = replace_weird_chars(text)
            id_comment = comment["id"]
            try:
                j = j+1
                if j < 51:
                    n_comments_, n_likes_ = get_summary_comment(id_comment, index_token)
                    best_comments.append((text, n_likes_, n_comments_))

            except Exception as e:
                logger.warning(str(e))
                if len(comments) > 1000:
                    logger.warning("Skipping error as I have enough comments (get summary)")
                    break

            comments.append(text)

        # check if there are more comments
        if 'paging' in data and 'next' in data['paging']:
            r = requests.get(data['paging']['next'])

            at = len(comments) / n_comments
            at = at * 100.0
            if at > 100 or at < 0:
                logger.info("Facebook sleeping: " + str(len(comments)))
                logger.info("scaricati " + str(at))
                logger.info("Post: " + message)
                logger.info("#Commenti: " + str(n_comments) + "\n\n")
            sleep(int(60 * delay))
        else:
            break

    couple, word_used_more, triple = tokenize(comments, message, page)
    first_word_used = word_used_more[0][0]
    first_word_used_count = word_used_more[0][1]
    s_word_used = word_used_more[1][0]
    s_word_used_count = word_used_more[1][1]
    t_word_used = word_used_more[2][0]
    t_word_used_count = word_used_more[2][1]
    forth_word_used = word_used_more[3][0]
    forth_word_used_count = word_used_more[3][1]
    fiveth_word_used = word_used_more[4][0]
    fiveth_word_used_count = word_used_more[4][1]

    try:
        first_couple_used = couple[0][0] + ' | ' + couple[0][1]
    except Exception:
        first_couple_used = None
    try:
        second_couple_used = couple[1][0] + ' | ' + couple[1][1]
    except:
        second_couple_used = None
    try:
        third_couple_used = couple[2][0] + ' | ' + couple[2][1]
    except:
        third_couple_used = None

    try:
        first_triplette_used = triple[0][0] + '|' + triple[0][1] + "|" + triple[0][2]
    except:
        first_triplette_used = None

    try:
        second_triplette_used = triple[1][0] + '|' + triple[1][1] + "|" + triple[1][2]
    except:
        second_triplette_used = None

    try:
        third_triplette_used = triple[2][0] + '|' + triple[2][1] + "|" + triple[2][2]
    except:
        third_triplette_used = None

    hashtags = get_hashtags(comments)

    try:
        first_hashtag_used = hashtags[0][0]
        first_hashtag_used_count = hashtags[0][1]
    except:
        first_hashtag_used_count = 0
        first_hashtag_used = None

    try:
        second_hashtag_used = hashtags[1][0]
        second_hashtag_used_count = hashtags[1][1]
    except:
        second_hashtag_used_count = 0
        second_hashtag_used = None
    topic = None
    sentiment = None
    best_comments = sorted(best_comments, key=lambda x : x[1], reverse=True)[0:3]
    insertFacebook(page, id_post, message, c_time, first_word_used, first_word_used_count,
                   s_word_used, s_word_used_count, t_word_used,
                   t_word_used_count, forth_word_used,
                   forth_word_used_count,
                   fiveth_word_used, fiveth_word_used_count,
                   first_couple_used,
                   second_couple_used, third_couple_used,
                   first_triplette_used,
                   second_triplette_used, third_triplette_used, n_comments, n_likes,
                   first_hashtag_used, first_hashtag_used_count, second_hashtag_used,
                   second_hashtag_used_count,
                   best_comments[0][0], best_comments[0][1], sentiment, topic,
                   best_comments[1][0], best_comments[1][1], best_comments[2][0], best_comments[2][1]
                   )
