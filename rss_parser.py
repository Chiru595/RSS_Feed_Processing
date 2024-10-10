# rss_parser.py
import feedparser
from datetime import datetime
from database_setup import NewsArticle, Session

def parse_feed(feed_url):
    feed = feedparser.parse(feed_url)
    articles = []
    for entry in feed.entries:
        article = {
            'title': entry.title,
            'content': entry.get('summary', ''),
            'pub_date': datetime(*entry.published_parsed[:6]),
            'url': entry.link
        }
        articles.append(article)
    return articles

def store_article(article):
    session = Session()
    if not session.query(NewsArticle).filter_by(url=article['url']).first():
        new_article = NewsArticle(
            title=article['title'],
            content=article['content'],
            pub_date=article['pub_date'],
            url=article['url'],
            category=article.get('category', 'Uncategorized')
        )
        session.add(new_article)
        session.commit()
    session.close()
