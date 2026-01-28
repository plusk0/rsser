from newspaper.utils import memoize_articles
import pandas as pd
from sqlalchemy import create_engine
from config.settings import Settings
import logging
import feedparser
import time
import random
import newspaper
from newspaper import Article, Config

logger = logging.getLogger(__name__)
analyzed_articles = (
    set()
)  # Tracked analyzed articles in in-memory-set for testing, will be in db table

### Dev mode feeds ###
feed_urls = [
    # "http://bbci.co.uk",
    # "http://abcnews.go.com",  # doesnt seem to work with morss
    # "http://aljazeera.com/",
    # "http://www.france24.com",
    # "http://www.derstandard.at/",
    # "http://www.france24.com/en/",
    "http://cnn.com",
]


def fetch_new_articles():
    if Settings.DEV_MODE:
        logger.info("Continuing in dev mode")
        return _fetch_articles(feed_urls)
    else:
        return _fetch_from_db()


# Start of freshRSS implementation code
# UPDATE: due to differences in performance/features, morss was switched out for newspaper3k
# Where morss was using dataframes via feedparser, here we use newspaper3k structure plus preprocessing
# License is APACHE2 due to high python-goose code use
# TODO: Filter interesting articles by summary/tags before nlp
def _fetch_articles(source_urls):
    """
    Takes a list/set of URLs
    Returns a dict of cleaned Article Title:Text entries (for testing, will use article object later)
    """
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/573.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"
    config = newspaper.Config()
    config.browser_user_agent = user_agent
    config.request_timeout = 10

    articles = dict()

    for url in source_urls:
        try:
            source = newspaper.build(url, config=config, memoize_articles=False)
            logger.info(f"Processing source: {url}")
            articlenr = 0
            for article in source.articles:
                if articlenr > 5:
                    print("Exceeded 5 articles per source")  # for testing only
                    break
                try:
                    article.download()
                    time.sleep(
                        0.1 + random.random() / 5
                    )  # Random delay between 0.1 and 0.3 seconds to limit ddos similarity and bot banning
                    article.parse()
                    articles[article.url] = article.text
                    logger.info(f"Successfully fetched article: {article.url}")
                    articlenr += 1
                except Exception as e:
                    logger.error(f"Failed to fetch article {article.url}: {e}")

        except Exception as e:
            logger.error(f"Failed to process source {url}: {e}")

    return articles


def _fetch_from_db():
    try:
        engine = create_engine(Settings.DB_URI)
        query = _build_query()
        return pd.read_sql(query, engine)
    except Exception as e:
        logger.error(f"Failed to fetch articles: {e}")
        return pd.DataFrame()


def _build_query():
    if analyzed_articles:
        query = f"""
                SELECT
                    e.id AS article_id,
                    e.title AS article_title,
                    e.content AS article_content,
                    e.link AS article_link,
                    e.date AS article_date,
                    f.name AS feed_name,
                    c.name AS category_name
                FROM
                    plusko_entry e
                JOIN
                    plusko_feed f ON e.id_feed = f.id
                LEFT JOIN
                    plusko_category c ON f.category = c.id
                WHERE
                    e.date > EXTRACT(EPOCH FROM NOW() - INTERVAL '7 days')
                    AND e.id NOT IN ({",".join(str(id) for id in analyzed_articles)})
                ORDER BY
                    e.date DESC;
                """
    # If no articles have been analyzed yet, remove the NOT IN clause
    else:
        query = """
        SELECT
            e.id AS article_id,
            e.title AS article_title,
            e.content AS article_content,
            e.link AS article_link,
            e.date AS article_date,
            f.name AS feed_name,
            c.name AS category_name
        FROM
            plusko_entry e
        JOIN
            plusko_feed f ON e.id_feed = f.id
        LEFT JOIN
            plusko_category c ON f.category = c.id
        WHERE
            e.date > EXTRACT(EPOCH FROM NOW() - INTERVAL '7 days')
        ORDER BY
            e.date DESC;
        """
    return query
