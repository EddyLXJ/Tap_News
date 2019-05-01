import requests
import os
import random

from lxml import html
GET_CNN_NEWS_XPATH = '''//p[@class="zn-body__paragraph"]//text() | //div[@class="zn-body__paragraph"]//text()'''
USER_AGENTS_FILE = os.path.join(os.path.dirname(__file__), 'user_agents.txt')
USER_AGENTS = []
with open(USER_AGENTS_FILE, 'r') as uaf:
    for ua in uaf.readlines():
        if ua:
            USER_AGENTS.append(ua.strip()[:])
random.shuffle(USER_AGENTS)

def getHeaders():
    us = random.choice(USER_AGENTS)
    print us
    headers = {
        "Connection" : "close",
        "User-Agent" : us
    }
    return headers

def extract_news(new_url):
    # Fetch html
    session_requests = requests.session()
    response = session_requests.get(new_url, headers = getHeaders())
    # Parse html
    news = {}
    try:
        tree = html.fromstring(response.content)
        news = tree.xpath(GET_CNN_NEWS_XPATH)
        news = ''.join(news)
    except Exception as e:
        print e
        return {}
    # Extract_information
    return news
