import pandas as pd
from sqlalchemy import create_engine
from config.settings import Settings
import logging
import feedparser
import morss

logger = logging.getLogger(__name__)
analyzed_articles = (
    set()
)  # Tracked analyzed articles in in-memory-set for testing, will be in db table

### Dev mode feeds ###
feed_urls = [
    # "https://feeds.bbci.co.uk/news/rss.xml",
    # "https://abcnews.go.com/abcnews/internationalheadlines",  # doesnt seem to work with morss
    "aljazeera.com/xml/rss/all.xml",
    # "france24.com/en/rss",
]


def fetch_new_articles():
    if Settings.DEV_MODE:
        logger.info("Continuing in dev mode")
        # return _load_mock_articles()
        return _combine_multiple_rss_feeds(feed_urls)
    else:
        return _fetch_from_db()


# Start of freshRSS implementation code
# TODO: Filter interesting articles by summary/tags, then fetch full text via morss
def _combine_multiple_rss_feeds(feed_urls):
    dfs = []
    print(f"No of urls:{len(feed_urls)}")
    for url in feed_urls:
        try:
            options = morss.Options(
                indent=True,
                FORCE=True,  # Disable caching and force refetch
                MAX_ITEM=100,  # Increase the number of articles fetched
                RESOLVE=True,  # Replace tracking links with direct links
                CLIP=True,  # Ensure full-text extraction
                # MODE="html",  # Use HTML parsing mode
                FIRSTLINK=True,  # Pull the first article link
                DEBUG=1,  # Enable debugging
            )
            url, rss = morss.FeedFetch(url, options)  # this only grabs the RSS feed
            rss = morss.FeedGather(
                rss, url, options
            )  # this fills the feed and cleans it up
            output = morss.FeedFormat(rss, options, "unicode")

            # logger.info(output)
            with open("testxml.xml", "w") as f:
                f.write(output)
            feed = feedparser.parse(output)
            dfs.append(pd.DataFrame(feed.entries))
        except Exception as e:
            print(f"Failed to fetch {url}: {e}")
    combined_df = pd.concat(dfs, ignore_index=True)
    return combined_df


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
