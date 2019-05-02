# -*- coding: utf-8 -*-

'''
Time decay model:

If selected:
p = (1-a) * p + a

If not:
p = (1 - a) * p

'''

import news_classes
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import mongodb_client
from cloudAMQP_client import CloudAMQPClient

NUM_OF_CLASSES = 17
INIFIAL_P = 1.0 / NUM_OF_CLASSES
ALPHA = 0.1

SLEEP_TIME_IN_SECONDS = 1

LOG_CLICKS_TASK_QUEUE_URL = "amqp://iexlisxy:9s18YA43iqNcjIVhxdBhaq269Kw0gqwn@crocodile.rmq.cloudamqp.com/iexlisxy"
LOG_CLICKS_TASK_QUEUE_NAME = "tap-news-log-clicks-task-queue"

PREFERENCE_MODEL_TABLE_NAME = "user_preference_model"
NEWS_TABLE_NAME = "news"

cloudAMQP_client = CloudAMQPClient(LOG_CLICKS_TASK_QUEUE_URL, LOG_CLICKS_TASK_QUEUE_NAME)

def handle_message(msg):
    if msg is None or not isinstance(msg, dict):
        return

    if 'userId' not in msg or 'newsId' not in msg or 'timestamp' not in msg:
        return
    userId = msg['userId']
    newsId = msg['newsId']

    db = mongodb_client.get_db()
    model = db[PREFERENCE_MODEL_TABLE_NAME].find_one({'userId': userId})

    # if Model not exist, create a new one
    if model is None:
        print 'Creating Preference model for new user: %s' % userId
        new_model = {'userId': userId}
        preference = {}
        for i in news_classes.classes:
            preference[i] = float(INIFIAL_P)
        new_model['preference'] = preference
        model = new_model

    print 'Updating preference model for new user: %s' % userId

    news = db[NEWS_TABLE_NAME].find_one({'digest': newsId})
    if news is None or 'class' not in news or news['class'] not in news_classes.classes:
        print news is None
        print 'class' not in news
        print news['class'] not in news_classes.classes
        print 'Skipping processing...'
        return

    click_class = news['class']

    old_p = model['preference'][click_class]
    model['preference'][click_class] = float((1 - ALPHA) * old_p + ALPHA)

    for i, prob in model['preference'].iteritems():
        if not i == click_class:
            model['preference'][i] = float((1 - ALPHA) * model['preference'][i])

    db[PREFERENCE_MODEL_TABLE_NAME].replace_one({'userId': userId}, model, upsert=True)

def run():
    while True:
        if cloudAMQP_client is not None:
            msg = cloudAMQP_client.getMessage()
            if msg is not None:
                try:
                    handle_message(msg)
                except Exception as e:
                    print e
                    pass

            cloudAMQP_client.sleep(SLEEP_TIME_IN_SECONDS)

if __name__ == "__main__":
    run()
