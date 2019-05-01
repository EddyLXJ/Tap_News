import mongodb_client as client

def test_basic():
    db = client.get_db('tap-news')
    db.news.drop()

    db['news'].insert({
        'url':'https://www.cnn.com/2019/04/21/asia/sri-lanka-explosions/index.html',
        'title':"Bombs tear through Sri Lankan churches and hotels, killing more than 200 people",
        'description':"The calm of Easter Sunday was shattered by gruesome bombings that killed at least 207 people in Sri Lankan churches and hotels.",
        'source':'cnn',
        'urlToImage':'https://cdn.cnn.com/cnnnext/dam/assets/190421114253-statue-of-jesus-from-sri-lanka-st-sebastians-church-medium-plus-169.jpg',
        'digest':"afsdasfd",
        'reason':"Recommend"
    })
    # db.news.insert({
    #     'url':'https://www.cnn.com/2019/04/21/opinions/william-barr-mueller-report-credibility-gutter-honig/index.html',
    #     'title':"William Barr threw his credibility in the gutter",
    #     'description':"Special Counsel Robert Mueller's report has arrived. While the report is more than 400 pages long, it raises countless new questions -- so many, in fact, that we decided to run a special installment of Cross-exam to answer them. Let's dig in.",
    #     'source':'bbc',
    #     'urlToImage':'https://cdn.cnn.com/cnnnext/dam/assets/190401142350-elie-honig-profile-medium-plus-169.jpg',
    #     'digest':"asdfasdf",
    #     'time':"Today",
    #     'reason':"Hot"
    # })

    assert db.news.count() == 1
    # db.news.drop()
    # assert db.news.count() == 0
    print 'test_basic passed'

if __name__ == "__main__":
    test_basic()
