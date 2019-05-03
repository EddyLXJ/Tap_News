# -*- coding utf-8 -*-
import os
import sys
import datetime

from dateutil import parser
from sklearn.feature_extraction.text import TfidfVectorizer

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import news_topic_modeling_service_client
import mongodb_client
from cloudAMQP_client_python import CloudAMQPClient

DEDUPE_NEXS_TASK_QUEUE_URL = "amqp://bxpjqpbr:zrevZ4ebxX4SrWME36DkefBfaMkNZx48@llama.rmq.cloudamqp.com/bxpjqpbr"
DEDUPE_NEXS_TASK_QUEUE_NAME = "tap-news-scrape-news-task-queue"

SLEEP_TIME_IN_SECONDS = 1

NEWS_TABLE_NAME = "news"

SAME_NEWS_SIMILARITY_THRESHOLD = 0.8

cloudAMQP_client = CloudAMQPClient(DEDUPE_NEXS_TASK_QUEUE_URL, DEDUPE_NEXS_TASK_QUEUE_NAME)

def handle_message(msg):
    if msg is None or not isinstance(msg, dict):
        return
    print(1)
    task = msg
    print(2)
    text = str(task['text'].encode('utf-8'))
    if text is None:
        return
    #Get all recent news:
    print(3)
    published_at = parser.parse(task['publishedAt'])
    print(4)
    published_at_day_begin = datetime.datetime(published_at.year, published_at.month, published_at.day, 0, 0, 0, 0)
    print(5)
    published_at_day_end = published_at_day_begin + datetime.timedelta(days=1)
    print(6)
    db = mongodb_client.get_db()

    recent_news_list = list(db[NEWS_TABLE_NAME].find(
        {'publishedAt':
            {'$gte': '%s' % (published_at_day_begin),
            '$lt': '%s' % (published_at_day_end)
            }
        }
        # db.news.find({'publishedAt': {'$gte': '2019-04-30T0:0:0Z', '$lt': '2019-05-01T0:0:0Z'}})
        )
    )
    print(published_at)
    print(published_at_day_begin)
    print(published_at_day_end)
    print(recent_news_list)

    if recent_news_list is not None and len(recent_news_list) > 0:
        print('8')
        documents = [str(news['text'].encode('utf-8')) for news in recent_news_list]
        print('&')
        documents.insert(0, text)
        print('9')
        # Calcul similarity
        tfidf = TfidfVectorizer().fit_transform(documents)
        pairwise_sim = tfidf * tfidf.T
        print(pairwise_sim)
        rows, _= pairwise_sim.shape
        for row in range(1, rows):
            if pairwise_sim[row, 0] > SAME_NEWS_SIMILARITY_THRESHOLD:
                print('Duplicated news. Ignore.')
                return
    # task['publishedAt'] = parser.parse(task['publishedAt'])

    title = task['title']
    if title is not None:
        topic = news_topic_modeling_service_client.classify(title)
        task['class'] = topic

    # db[NEWS_TABLE_NAME].insert(task)
    db[NEWS_TABLE_NAME].replace_one({'digest': task['digest']}, task, True)


while True:
    if cloudAMQP_client is not None:
        msg = cloudAMQP_client.getMessage()
        if msg is not None:
            try:
                handle_message(msg)
            except Exception as e:
                print(e)
                pass
        cloudAMQP_client.sleep(SLEEP_TIME_IN_SECONDS)
