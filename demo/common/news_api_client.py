import requests
from json import loads
import json

NEWS_API_ENDPOINT = 'https://newsapi.org/v2/'
NEWS_API_KEY = 'efabc3e32bbf466083e909e626150e43'
ARTICALS_API = 'top-headlines'

CNN = 'cnn'
DEFAULT_SOURCES = [CNN]
def buildUrl(end_point = NEWS_API_ENDPOINT, api_name=ARTICALS_API):
    return end_point + api_name

def getNewsFromSource(sources=DEFAULT_SOURCES):
    articles = []
    for source in sources:
        payload = {'apiKey' : NEWS_API_KEY,
                    'sources' : source}
        response = requests.get(buildUrl(), params = payload)
        res_json = json.loads(response.content.decode('utf-8'))

        if(res_json is not None and res_json['status'] == 'ok' and res_json['totalResults'] != 0):
            for news in res_json['articles']:
                source = news['source']['name']
                news['source'] = source
            articles.extend(res_json['articles'])
    return articles
