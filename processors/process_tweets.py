from DB.utility import insert
from processors.parsing import tokenize, get_hashtags, get_comment_most_liked
import re


def replace_weird_chars(input):
    message = input.lower()
    message = message.replace("à", "a'").replace("è", "e'").replace("ù", "u'").replace("ì", "i'").replace("ò",
                                                                                                          "o'").replace(
        'é', 'e').replace("”", "\"") \
        .replace("😁", "").replace("’", "'").replace("ú", "u'").replace("«", "").replace("»", "", ).replace("💔",
                                                                                                            "").replace(
        "🦍", "").replace("🔴", "").replace("”", "").replace("“", "").replace("💪", "").replace("🍕", "").replace("😂",
                                                                                                                  "").replace(
        "😉", "").replace("😀", "").replace("🤮", "").replace("🤢", "").replace("°", "").replace("💩", "").replace("⭐",
                                                                                                                   "").replace(
        "😊", "").replace("🌟", ""). \
        replace("🏆", "").replace("🇮", "").replace("🇹", "").replace("😱", "").replace("🤞", "").replace("🤡", "").replace("🤦‍", '').replace("♀", '').\
        replace("🤦", "")

    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               "]+", flags=re.UNICODE)
    message = emoji_pattern.sub(r'', message)
    message = message.replace("\\xF0\\x9F\\xA4\\x9E", "")
    return message


def process_source_and_replies(source, replies, page):
    comments = [x.full_text.replace(page, "") for x in replies]
    comments = [replace_weird_chars(x) for x in comments]
    id_source = source.id
    title = replace_weird_chars(source.full_text)
    created_at = source.created_at
    couple, word_used_more, triple = tokenize(comments, title, page)
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

    comment, num = get_comment_most_liked(replies)
    comment = replace_weird_chars(comment)
    comment_sentiment = None
    topic = None

    num_reply_post = len(comments)
    num_likes_post = source.favorite_count
    num_retweet_post = source.retweet_count

    insert(page,id_source, title, created_at, first_word_used, first_word_used_count,
           s_word_used, s_word_used_count, t_word_used,
           t_word_used_count, forth_word_used,
           forth_word_used_count,
           fiveth_word_used, fiveth_word_used_count,
           first_couple_used,
           second_couple_used, third_couple_used,
           first_triplette_used,
           second_triplette_used, third_triplette_used, num_reply_post, num_likes_post,
           num_retweet_post,
           first_hashtag_used, first_hashtag_used_count, second_hashtag_used,
           second_hashtag_used_count,
           comment, num, comment_sentiment, topic)
    print("inserted")
