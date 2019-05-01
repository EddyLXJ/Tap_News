import cnn_news_scraper as scraper

EXPECTED_NEWS = "The case is one of the few legal tests of the constitutional clause -- yet is among several suits that contest Trump's family business while he's in the White House."
CNN_NEWS_URL = "https://www.cnn.com/2019/04/30/politics/emoluments-lawsuit-congress/index.html"

def test_basic():
    news = scraper.extract_news(CNN_NEWS_URL)
    assert EXPECTED_NEWS in news
    print 'test_basic passed'

if __name__ == "__main__":
    test_basic()
