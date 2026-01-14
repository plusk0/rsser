import pandas as pd
from sqlalchemy import create_engine
from config.settings import Settings
import logging
import json
import random

logger = logging.getLogger(__name__)
analyzed_articles = (
    set()
)  # Tracked analyzed articles in in-memory-set for testing, should be in db table


def fetch_new_articles():
    if Settings.DEV_MODE:
        logger.info("Continuing in dev mode")
        return _load_mock_articles()
    else:
        return _fetch_from_db()


def _load_mock_articles():
    try:
        with open("./testing/mock_articles.json", "r") as f:
            data = json.load(f)
        return pd.DataFrame(_adapt_rss_items(data["items"]))
    except Exception as e:
        logger.error(f"Failed to load mock articles: {e}")
        return pd.DataFrame()


def _fetch_from_db():
    try:
        engine = create_engine(Settings.DB_URI)
        query = _build_query()
        return pd.read_sql(query, engine)
    except Exception as e:
        logger.error(f"Failed to fetch articles: {e}")
        return pd.DataFrame()


def _build_query():
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
    if not analyzed_articles:
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


def _adapt_rss_items(items):
    adapted_items = []
    for item in items:
        # Flatten the enclosure object
        enclosure_link = item.get("enclosure", {}).get("link", "")

        # Convert categories list to a string
        categories_str = ", ".join(item.get("categories", []))

        # Create a new dictionary with flattened fields
        adapted_item = {
            "article_id": random.randint(1, 999999),
            "article_title": item.get("title", ""),
            "article_date": item.get("pubDate", ""),
            "article_link": item.get("link", ""),
            "guid": item.get("guid", ""),
            "author": item.get("author", ""),
            "thumbnail": item.get("thumbnail", ""),
            "description": item.get("description", ""),
            "article_content": item.get("content", ""),
            "enclosure_link": enclosure_link,
            "category_name": categories_str,
        }
        adapted_items.append(adapted_item)
    return adapted_items
