import MySQLdb

from DB.schema import schema


def insert(table,
           id_source_twit, title, time, first_word_most_used_in_comments, first_word_most_used_in_comments_count,
           second_word_most_used_in_comments, second_word_most_used_in_comments_count, third_word_most_used_in_comments,
           third_word_most_used_in_comments_count, fourth_word_most_used_in_comments,
           fourth_word_most_used_in_comments_count,
           fiveth_word_most_used_in_comments, fiveth_word_most_used_in_comments_count,
           first_couple_words_most_used_in_comments,
           second_couple_words_most_used_in_comments, third_couple_words_most_used_in_comments,
           first_3_words_most_used_in_comments,
           second_3_words_most_used_in_comments, third_3_words_most_used_in_comments, num_reply_post, num_likes_post,
           num_retweet_post,
           first_hashtag_most_used, first_hashtag_most_used_count, second_hashtag_most_used,
           second_hashtag_most_used_count,
           comment_with_most_likes, likes_to_most_comment, comment_sentiment, topic):
    table = table.replace(".", "")
    conn = MySQLdb.connect(host="localhost",
                           user="enrico",
                           passwd="quaglia", init_command="set names utf8",
                           db="twitter", use_unicode=True
                           )

    id_source_twit = str(id_source_twit)
    x = conn.cursor()
    x.execute("SET NAMES utf8mb4;")  # or utf8 or any other charset you want to handle

    x.execute("SET CHARACTER SET utf8mb4;")  # same as above

    x.execute("SET character_set_connection=utf8mb4;")

    query_check = "SELECT count(*) FROM " + table + " where id_source_twit=\"" + id_source_twit + "\""

    x.execute(query_check)
    res = x.fetchall()[0]

    if res[0] != 0:
        x.execute("delete from " + table + " where id_source_twit=\"" + id_source_twit + "\"")
        conn.commit()

    try:
        ret = x.execute(" INSERT INTO " + table + """ VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s  )""", (
            id_source_twit, title, time, first_word_most_used_in_comments, first_word_most_used_in_comments_count,
            second_word_most_used_in_comments, second_word_most_used_in_comments_count,
            third_word_most_used_in_comments,
            third_word_most_used_in_comments_count, fourth_word_most_used_in_comments,
            fourth_word_most_used_in_comments_count,
            fiveth_word_most_used_in_comments, fiveth_word_most_used_in_comments_count,
            first_couple_words_most_used_in_comments,
            second_couple_words_most_used_in_comments, third_couple_words_most_used_in_comments,
            first_3_words_most_used_in_comments,
            second_3_words_most_used_in_comments, third_3_words_most_used_in_comments, num_reply_post, num_likes_post,
            num_retweet_post,
            first_hashtag_most_used, first_hashtag_most_used_count, second_hashtag_most_used,
            second_hashtag_most_used_count,
            comment_with_most_likes, likes_to_most_comment, comment_sentiment, topic
        ))
        conn.commit()
    except Exception as e:
        print("ERROR DB ")
        print(e)
        print(title)
        print(comment_with_most_likes)
        conn.rollback()

    conn.close()


def show_tables(db='twitter'):
    conn = MySQLdb.connect(host="localhost",
                           user="enrico",
                           passwd="quaglia", init_command="set names utf8",
                           db=db, use_unicode=True
                           )
    query_check = "show tables"
    x = conn.cursor()
    x.execute(query_check)
    res = x.fetchall()
    return [i[0] for i in res]


def get_nulls(table, db='twitter'):
    conn = MySQLdb.connect(host="localhost",
                           user="enrico",
                           passwd="quaglia", init_command="set names utf8",
                           db=db, use_unicode=True
                           )
    table = table.replace(".", "")
    query = "Select * from " + table + " where topic is null order by time desc"
    x = conn.cursor()
    x.execute(query)
    res = x.fetchall()
    schema_list = [x.replace(" ", "") for x in schema.split(",")]
    to_return = []
    for row in res:
        d = {'page': table}
        for index, field in enumerate(schema_list):
            d[field] = row[index]
        to_return.append(d)
    return to_return


def update_db(data):
    table = data['page']
    table = table.replace(".", "")
    db = data['db']
    id = str(data['id'])
    sentiment = str(data['sent'])
    topic = data['topic']
    conn = MySQLdb.connect(host="localhost",
                           user="enrico",
                           passwd="quaglia", init_command="set names utf8",
                           db=db, use_unicode=True
                           )
    if db == 'twitter':
        query = "UPDATE " + table + " SET topic = " + "'" + topic + "'" + " WHERE id_source_twit = " + id
    else:
        query = "UPDATE " + table + " SET topic = " + "'" + topic + "'" + " WHERE id = " + id
    x = conn.cursor()
    x.execute(query)

    if db == 'twitter':
        query = "UPDATE " + table + " SET comment_sentiment = " + "'" + sentiment + "'" + " WHERE id_source_twit = " + id
    else:
        query = "UPDATE " + table + " SET comment_sentiment = " + "'" + sentiment + "'" + " WHERE id = " + id
    x = conn.cursor()
    x.execute(query)
    try:
        conn.commit()
    except Exception as e:
        print("ERROR DB ")
        print(e)
        conn.rollback()
    conn.close()


def insertFacebook(table, id_post, message, c_time, first_word_most_used_in_comments,
                   first_word_most_used_in_comments_count,
                   second_word_most_used_in_comments,
                   second_word_most_used_in_comments_count, third_word_most_used_in_comments,
                   third_word_most_used_in_comments_count, fourth_word_most_used_in_comments,
                   fourth_word_most_used_in_comments_count,
                   fiveth_word_most_used_in_comments, fiveth_word_most_used_in_comments_count,
                   first_couple_words_most_used_in_comments, second_couple_words_most_used_in_comments,
                   third_couple_words_most_used_in_comments,
                   first_3_words_most_used_in_comments, second_3_words_most_used_in_comments,
                   third_3_words_most_used_in_comments, num_reply_post, num_likes_post,
                   first_hashtag_most_used, first_hashtag_most_used_count, second_hashtag_most_used,
                   second_hashtag_most_used_count,
                   comment_with_most_likes, likes_to_most_comment, sentiment, topic):
    conn = MySQLdb.connect(host="localhost",
                           user="enrico",
                           passwd="quaglia", init_command="set names utf8",
                           db="facebook", use_unicode=True
                           )
    table = table.replace(".", "")

    id_post = str(id_post)
    x = conn.cursor()
    x.execute("SET NAMES utf8mb4;")  # or utf8 or any other charset you want to handle

    x.execute("SET CHARACTER SET utf8mb4;")  # same as above

    x.execute("SET character_set_connection=utf8mb4;")

    query_check = "SELECT count(*) FROM " + table + " where id=\"" + id_post + "\""

    x.execute(query_check)
    res = x.fetchall()[0]

    if res[0] != 0:
        x.execute("delete from " + table + " where id=\"" + id_post + "\"")
        conn.commit()

    try:
        ret = x.execute(" INSERT INTO " + table + """ VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s  )""", (
            id_post, message, c_time, first_word_most_used_in_comments, first_word_most_used_in_comments_count,
            second_word_most_used_in_comments, second_word_most_used_in_comments_count,
            third_word_most_used_in_comments,
            third_word_most_used_in_comments_count, fourth_word_most_used_in_comments,
            fourth_word_most_used_in_comments_count,
            fiveth_word_most_used_in_comments, fiveth_word_most_used_in_comments_count,
            first_couple_words_most_used_in_comments,
            second_couple_words_most_used_in_comments, third_couple_words_most_used_in_comments,
            first_3_words_most_used_in_comments,
            second_3_words_most_used_in_comments, third_3_words_most_used_in_comments, num_reply_post, num_likes_post,
            first_hashtag_most_used, first_hashtag_most_used_count, second_hashtag_most_used,
            second_hashtag_most_used_count,
            comment_with_most_likes, likes_to_most_comment, sentiment, topic
        ))
        conn.commit()
    except Exception as e:
        print("ERROR DB ")
        print(e)
        print(message)
        print(comment_with_most_likes)
        conn.rollback()
    print("Facebook done!")
    conn.close()
