# -*- coding utf-8 -*-
import os
import sys
# from newspaper.newspaper import Article

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'scrapers'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'newspaper-python-2-head/newspaper'))
from article import Article

from cloudAMQP_client_python import CloudAMQPClient

DEDUPE_NEXS_TASK_QUEUE_URL = "amqp://bxpjqpbr:zrevZ4ebxX4SrWME36DkefBfaMkNZx48@llama.rmq.cloudamqp.com/bxpjqpbr"
DEDUPE_NEXS_TASK_QUEUE_NAME = "tap-news-scrape-news-task-queue"
SCRAPE_NEWS_TASK_QUEUE_URL = "amqp://sijpefxd:bA3nwVVE10UXMNGmm6u9Po4W5QjslspG@llama.rmq.cloudamqp.com/sijpefxd"
SCRAPE_NEWS_TASK_QUEUE_NAME = "tap-news-scrape-news-task-queue"

SLEEP_TIME_IN_SECONDS = 5

dedupe_news_queue_client = CloudAMQPClient(DEDUPE_NEXS_TASK_QUEUE_URL, DEDUPE_NEXS_TASK_QUEUE_NAME)
scrape_news_queue_client = CloudAMQPClient(SCRAPE_NEWS_TASK_QUEUE_URL, SCRAPE_NEWS_TASK_QUEUE_NAME)

def handle_message(msg):
    if msg is None or not isinstance(msg, dict):
        print(message is broken)
        return

    task = msg

    article1 = Article(task['url'])
    article1.download()
    article1.parse()
    task['text'] = article1.text
    dedupe_news_queue_client.sendMessage(task)


while True:
    #Fetch msg from queue
    if scrape_news_queue_client is not None:
        msg = scrape_news_queue_client.getMessage()
        if msg is not None:
            try:
                handle_message(msg)
            except Exception as e:
                print(e)
                pass
        scrape_news_queue_client.sleep(SLEEP_TIME_IN_SECONDS)
