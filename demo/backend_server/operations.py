import json
import os
import pickle
import random
import redis
import sys

from bson.json_util import dumps
from datetime  import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
import mongodb_client
# import news_recommendation_service_client

from cloudAMQP_client import CloudAMQPClient

REDIS_HOST = "localhost"
REDIS_PORT = 6379

NEWS_TABLE_NAME = "news"
CLICK_LOGS_TABLE_NAME = 'click_logs'

NEWS_LIMIT = 100
NEWS_LIST_BATCH_SIZE = 10
USER_NEWS_TIME_OUT_IN_SECONDS = 600

LOG_CLICKS_TASK_QUEUE_URL = "amqp://iexlisxy:9s18YA43iqNcjIVhxdBhaq269Kw0gqwn@crocodile.rmq.cloudamqp.com/iexlisxy"
LOG_CLICKS_TASK_QUEUE_NAME = "tap-news-log-clicks-task-queue"

redis_client = redis.StrictRedis(REDIS_HOST, REDIS_PORT, db=0)
cloudAMQP_client = CloudAMQPClient(LOG_CLICKS_TASK_QUEUE_URL, LOG_CLICKS_TASK_QUEUE_NAME)

def getNewsSummariesForUser(user_id, page_num):
    print user_id, page_num
    if page_num <= 0:
        return None
    page_num = int(page_num)
    begin_index = (page_num - 1) * NEWS_LIST_BATCH_SIZE
    end_index = page_num * NEWS_LIST_BATCH_SIZE

    sliced_news = []

    if redis_client.get(user_id) is not None:
        news_digests = pickle.loads(redis_client.get(user_id))

        # If begin_index is out of range return empty list
        # If endindex is out of range return all remaining news
        sliced_news_digests = news_digests[begin_index:end_index]
        print(sliced_news_digests)
        db = mongodb_client.get_db()
        sliced_news = list(db[NEWS_TABLE_NAME].find({'digest':{'$in': sliced_news_digests}}))
    else:
        db = mongodb_client.get_db()
        total_news = list(db[NEWS_TABLE_NAME].find().sort([('publishedAt', -1)]).limit(NEWS_LIMIT))
        total_news_digests = map(lambda x:x['digest'], total_news)

        redis_client.set(user_id, pickle.dumps(total_news_digests))
        redis_client.expire(user_id, USER_NEWS_TIME_OUT_IN_SECONDS)

        sliced_news = total_news[begin_index:end_index]
    return json.loads(dumps(sliced_news))
