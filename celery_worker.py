# celery_worker.py
from celery import Celery
from rss_parser import parse_feed, store_article
from nlp_classifier import classify_article

app = Celery('news_collector', broker='redis://localhost:6379/0')

@app.task
def process_feed(feed_url):
    articles = parse_feed(feed_url)
    for article in articles:
        classify_and_store_article.delay(article)

@app.task
def classify_and_store_article(article):
    article['category'] = classify_article(article['content'])
    store_article(article)
