import random

from flask import Blueprint, jsonify
from flask import request

from DB.utility import show_tables, get_nulls, update_db

db_api = Blueprint('db_api', __name__)


def api_version(res, db):
    if db == 'facebook':
        id = 'id'
    else:
        id = 'id_source_twit'
    to_return = []
    for j in res:
        d = {}
        d['page'] = j['page']
        d['id'] = j[id]
        d['title'] = j['title']
        d['psu'] = j['first_word_most_used_in_comments'] + " | " + j['second_word_most_used_in_comments'] \
                   + " | " + j['third_word_most_used_in_comments']
        d['cp'] = j['first_couple_words_most_used_in_comments'] + " @ " + j['second_couple_words_most_used_in_comments']
        d['tripla'] = j['first_3_words_most_used_in_comments']
        d['ht'] = j['first_hashtag_most_used']
        d['commlikes'] = j['comment_with_most_likes']
        d['sec_com'] = j['second_comment']
        d['third_com'] = j['third_comment']
        d['db'] = db
        to_return.append(d)
    return to_return


@db_api.route("/return_all")
def return_all():
    dbs = ['facebook', 'twitter']
    r = random.randint(1, 10)
    db = dbs[r % 2]
    tables = show_tables(db=db)
    count = 0
    to_return = []
    for i in tables:
        try:
            res = get_nulls(i, db=db)
        except:
            continue
        if not res:
            continue
        res = api_version(res, db)
        to_return += res
        count += len(res)
        if count > 10:
            break
    return jsonify(to_return)


@db_api.route("/send", methods=['POST'])
def send():
    data = request.json
    update_db(data)
    return jsonify("OK")
