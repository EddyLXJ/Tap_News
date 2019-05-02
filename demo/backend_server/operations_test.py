import operations
import os
import sys

from sets import Set

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
import mongodb_client

def test_getNewsSummariesForUser_Basic():
    news = operations.getNewsSummariesForUser('test', 1)
    print news
    assert len(news)>0
    print "test_getNewsSummariesForUser_Basic passed"

def test_getNewsSummariesForUser_pagination():
    news_page_1 = operations.getNewsSummariesForUser('test', 1)
    news_page_2 = operations.getNewsSummariesForUser('test', 2)

    assert len(news_page_1) > 0
    assert len(news_page_2) > 0

    digests_page_1_set = Set([news['digest'] for news in news_page_1])
    digests_page_2_set = Set([news['digest'] for news in news_page_2])

    assert len(digests_page_1_set.intersection(digests_page_2_set)) == 0
    print 'test_getNewsSummariesForUser_pagination passed'

if __name__ == '__main__':
    test_getNewsSummariesForUser_Basic()
    test_getNewsSummariesForUser_pagination()