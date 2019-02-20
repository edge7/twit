from nltk.collocations import BigramCollocationFinder
from nltk.collocations import TrigramCollocationFinder
from nltk.corpus import stopwords
from nltk.metrics import BigramAssocMeasures
from nltk.metrics import TrigramAssocMeasures
from nltk.tokenize import RegexpTokenizer
import re

from DB.utility import show_tables, get_posts, insert_post_analisi

to_filter_generic_ita = ['ciao', 'de', 'fa', 'cosa', 'così', 'solo', 'facebook', 'www', 'ora',
                         'https', 'poi', 'un\'altra',
                         'ancora', 'italiani', 'infatti', 'fare', 'mai', 'proprio', 'fatto', 'ciao', 'sempre', 'italia',
                         'e\'',
                         'navi', 'ministro', 'italia', 'x', 'php', 'story', 'facebook', 'story_fbid', 'youtube',
                         'popolo',
                         'italiano', 'già', 'è', 'analisi',
                         'essere', 'prima', 'senza', 'caso', 'dice', 'oggi', 'te', 'due', 'perche', 'quando'
                         ]

to_filter_generic_ame = ["hello", "hi", "us", "american", "would",
                         "america", "mr"
                         ]

to_filter_salvini = to_filter_generic_ita + ['matteo', 'salvini', 'ministro', 'sal', 'ni']
to_filter_dimaio = to_filter_generic_ita + ['maio', 'ministro', 'stelle', '5', 'luigi', 'lavoro']
to_filter_mentana = to_filter_generic_ita + ['direttore', 'enrico', 'mentana', 'la7', 'lavoro']

to_filter_trump = to_filter_generic_ame + ["president", "american", "donald", ]


def getLanguageFromPage(page):
    if 'trump' in page:
        return 'english'
    return 'italian'


def getToFilterFromPage(page):
    page = page.lower()
    if 'salvini' in page:
        return to_filter_salvini
    if 'dimaio' in page:
        return to_filter_dimaio
    if 'trump' in page:
        return to_filter_trump
    if 'mentana' in page:
        return to_filter_mentana

    return to_filter_generic_ita
    raise Exception("Error filtering")


def tokenize_post(message, page):
    language = getLanguageFromPage(page)
    to_filter = getToFilterFromPage(page)
    message = message.lower()
    words_list = []
    d = {}

    tokenizer = RegexpTokenizer("[\w']+")
    res = tokenizer.tokenize(message)
    for r in res:
        r = r.lower()
        words_list.insert(0, r)
        if r in set(stopwords.words(language) + to_filter):
            continue
        counter = d.get(r, 0)
        d[r] = counter + 1

    # print("\n\n Stampo le 4 parole più usate")
    # for item in sorted(d.items(), key=lambda x: x[1], reverse=True)[0:4]:
    #    print(item)

    # print(" \n\n Adesso stampo le parole che vanno più a coppia:")
    filter_stops = lambda w: len(w) < 3 or w in set(stopwords.words(language) + to_filter)
    bcf = BigramCollocationFinder.from_words(words_list)
    bcf.apply_word_filter(filter_stops)
    res_couple = bcf.nbest(BigramAssocMeasures.likelihood_ratio, 10)
    # print(res_couple)

    tcf = TrigramCollocationFinder.from_words(words_list)
    tcf.apply_word_filter(filter_stops)
    tcf.apply_freq_filter(3)
    res_triple = tcf.nbest(TrigramAssocMeasures.likelihood_ratio, 5)
    # print(" \n\n Adesso stampo la tripletta di parole più usato insieme:")
    # print(res_triple)

    return res_couple, sorted(d.items(), key=lambda x: x[1], reverse=True)[0:20], res_triple


def tokenize(comments, message, page):
    language = getLanguageFromPage(page)
    to_filter = getToFilterFromPage(page)
    message = message.lower()
    words_list = []
    d = {}
    for line in comments:
        tokenizer = RegexpTokenizer("[\w']+")
        res = tokenizer.tokenize(line)
        res = [x for x in res if len(x) > 2]
        for r in res:
            r = r.lower()
            words_list.insert(0, r)
            if r in set(stopwords.words(language) + to_filter) or r in message:
                continue
            counter = d.get(r, 0)
            d[r] = counter + 1

    # print("\n\n Stampo le 15 parole più usate")
    # for item in sorted(d.items(), key=lambda x: x[1], reverse=True)[0:15]:
    #    print(item)

    # print(" \n\n Adesso stampo le parole che vanno più a coppia:")
    filter_stops = lambda w: len(w) < 3 or w in set(stopwords.words(language) + to_filter)
    bcf = BigramCollocationFinder.from_words(words_list)
    bcf.apply_word_filter(filter_stops)
    res_couple = bcf.nbest(BigramAssocMeasures.likelihood_ratio, 10)
    # print(res_couple)

    tcf = TrigramCollocationFinder.from_words(words_list)
    tcf.apply_word_filter(filter_stops)
    tcf.apply_freq_filter(3)
    res_triple = tcf.nbest(TrigramAssocMeasures.likelihood_ratio, 5)

    return res_couple, sorted(d.items(), key=lambda x: x[1], reverse=True)[0:20], res_triple


def get_hashtags(comments):
    d = {}
    for com in comments:
        res = re.findall(r"#(\w+)", com.lower())
        for j in res:
            v = d.get(j, 0)
            d[j] = v + 1
    return sorted(d.items(), key=lambda x: x[1], reverse=True)[0:20]


def get_comments_most_liked(replies):
    replies = sorted([(r.full_text, r.favorite_count) for r in replies], key= lambda x: x[1], reverse=True)[0:3]
    return replies


def analyse_post():
    for db in ['twitter', 'facebook']:
        tables = show_tables(db=db)
        for table in tables:
            try:
                posts = get_posts(table, db)
            except:
                #print("Skipping Table " + table)
                continue
            if len(posts) < 5:
                continue
            posts = [x[0] for x in posts]
            couple, word_used_more, triple = tokenize(posts, table, table)
            if not word_used_more:
                continue
            first_word_used = word_used_more[0][0]
            first_word_used_count = word_used_more[0][1]
            s_word_used = word_used_more[1][0]
            s_word_used_count = word_used_more[1][1]
            t_word_used = word_used_more[2][0]
            t_word_used_count = word_used_more[2][1]

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
            insert_post_analisi(table, db, first_word_used, s_word_used, t_word_used,
                                first_word_used_count, s_word_used_count, t_word_used_count,
                                first_couple_used, second_couple_used, third_couple_used, first_triplette_used,
                                second_triplette_used)
