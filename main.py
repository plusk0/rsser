import logging
import time
from data.fetcher import fetch_new_articles
from processing.preprocessor import preprocess
from processing.statistical import analyze_lda

# from processing.transformer import summarize
# from processing.validator import validate_summary
from visualization.summary_vis import visualize_lda
from config.settings import Settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    while True:
        try:
            logger.info("Trying to find articles")
            df = fetch_new_articles()
            if not df.empty:
                logger.info(f"Fetched {len(df)} new articles.")
                texts = df["article_content"].apply(preprocess)
                texts = [text for text in texts if text]
                if texts:
                    lda, corpus, dictionary = analyze_lda(texts)
                    if lda:
                        visualize_lda(lda, corpus, dictionary)
                        logger.info("Visualizer Done!")
                        for idx, row in df.iterrows():
                            article_text = row["article_content"]
                            # Statistical summary (e.g., first sentence or LexRank)
                            statistical_summary = article_text.split(".")[0]
                            # Transformer summary (if in downtime or long article)
                            # if len(article_text.split()) > 500:
                            #    transformer_summary = summarize(article_text)
                            #    if transformer_summary and validate_summary(
                            #        article_text, transformer_summary
                            #    ):
                            #        compare_summaries(
                            #            article_text,
                            #            statistical_summary,
                            #            transformer_summary,
                            #        )
                            #    else:
                            #        logger.warning(
                            #            f"Transformer summary invalid for article {row['article_id']}."
                            #        )
                            Settings.ANALYZED_ARTICLES.add(row["article_id"])
                else:
                    logger.warning("No valid articles after preprocessing.")
            else:
                logger.info("No new articles. Running transformer on backlog...")
                # Optional: Process backlog or older articles with transformer
        except Exception as e:
            logger.error(f"Main loop error: {e}")
        logger.info("Loop done! Check output for visual representation")
        time.sleep(60)


if __name__ == "__main__":
    logger.info("hi")
    main()
