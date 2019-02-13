from flask import Blueprint, jsonify
from flask import request

from DB.utility import show_tables, get_nulls, update_db

db_api = Blueprint('db_api', __name__)


def api_version(res):
    to_return = []
    for j in res:
        d = {}
        d['page'] = j['page']
        d['id'] = j['id_source_twit']
        d['title'] = j['title']
        d['psu'] = j['first_word_most_used_in_comments'] + " | " + j['second_word_most_used_in_comments'] \
        + " | " + j['third_word_most_used_in_comments']
        d['cp'] = j['first_couple_words_most_used_in_comments'] + " @ " + j['second_couple_words_most_used_in_comments']
        d['tripla'] = j['first_3_words_most_used_in_comments']
        d['ht'] = j['first_hashtag_most_used']
        d['commlikes'] = j['comment_with_most_likes']
        to_return.append(d)
    return to_return

@db_api.route("/return_all")
def return_all():

    tables = show_tables()
    count = 0
    for i in tables:
        res = get_nulls(i)
        res= api_version(res)
        count += len(res)
        if count > 10:
            break
    return jsonify(res)

@db_api.route("/send", methods=['POST'])
def send():
    data = request.json
    update_db(data)
    return jsonify("OK")