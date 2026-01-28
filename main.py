import logging
import time
from data.fetcher import fetch_new_articles
from processing.preprocessor import (
    preprocess_for_lda,
    preprocess_for_textrank,
)
from processing.statistical import analyze_lda, summarize_text
import pandas as pd
from nltk.tokenize import word_tokenize, sent_tokenize

# from processing.transformer import summarize
# from processing.validator import validate_summary
from visualization.summary_vis import visualize_lda
from config.settings import Settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    summaries = dict()
    print("Starting rsser...\n-----", end="\r")

    while True:
        try:
            logger.info("Trying to find articles\n-----")
            x = 0
            data = fetch_new_articles()
            logger.info(f"Found {len(data)} new articles")
            # with open("testxml.xml", "w") as f:
            #   f.write("\n\n".join(data))

            texts = data.copy()

            if data:
                lda_data = [preprocess_for_lda(text) for url, text in data.items()]
                lda_data = [text for text in lda_data if text]

                if lda_data:
                    lda, corpus, dictionary = analyze_lda(lda_data)
                    if lda:
                        visualize_lda(lda, corpus, dictionary)
                        logger.info("Visualizer Done!")

            if texts:
                for url, text in texts.items():
                    sentences = sent_tokenize(text)
                    if sentences:
                        summary = summarize_text(sentences)
                        summaries[url] = summary  ### TODO: Meta-summary ?

            else:
                logger.info("No new articles. Running transformer on backlog...")
                # TODO: Process backlog or older articles with transformer
        except Exception as e:
            logger.error(f"Main loop error: {e}")
        logger.info("Loop done! Check output for visual representation")
        logger.info("Summaries:")
        output = "\r"
        print(summaries)
        for url, summary in summaries.items():
            output += f"{url}:\n{summary}\n----------\n"
        print(f"{output}", end="\r")
        time.sleep(60)


if __name__ == "__main__":
    main()
