import news_topic_modeling_service_client as client

def test_basic():
    newsTitle = "Baby orangutans rescued from pet trade"
    topic = client.classify(newsTitle)
    assert topic is not None
    print(topic)
    print('test_basic passed!')

if __name__ == "__main__":
    test_basic()
