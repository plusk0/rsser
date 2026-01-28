import logging
import time
from data.fetcher import fetch_new_articles
from processing.preprocessor import (
    preprocess_for_lda,
    preprocess_for_textrank,
)
from processing.statistical import analyze_lda, summarize_text
import pandas as pd

# from processing.transformer import summarize
# from processing.validator import validate_summary
from visualization.summary_vis import visualize_lda
from config.settings import Settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    summaries = {}
    pd.set_option(
        "display.max_rows", None
    )  # Show all/more rows for debugging/logging df in console
    pd.set_option("display.max_columns", None)
    print("Starting rsser...\n-----", end="\r")
    while True:
        try:
            logger.info("Trying to find articles\n-----")
            df = fetch_new_articles()
            if not df.empty:
                print(f"\rFetched {len(df['title'])} new articles.\n-----")
                df["text"] = df["content"].apply(
                    lambda x: x[0]["value"]
                    if isinstance(x, list) and len(x) > 0 and "value" in x[0]
                    else ""
                )
                df["text"] = df["text"].fillna(df["summary"])
                # Extract text from df with fallback to summary

                data = df["text"].to_list()
                texts = data.copy()
                if data:
                    lda_data = [preprocess_for_lda(text) for text in data]
                    lda_data = [text for text in lda_data if text]

                    if lda_data:
                        lda, corpus, dictionary = analyze_lda(lda_data)
                        if lda:
                            visualize_lda(lda, corpus, dictionary)
                            logger.info("Visualizer Done!")
                if texts:
                    ### Statistical summary via TextRank ###
                    for text in texts:
                        title, sentences = preprocess_for_textrank(text)
                        if sentences:
                            summaries[summarize_text(title, sentences)] = 1
                        ### TODO: Meta-summary ?

                        for idx, row in df.iterrows():
                            # TODO: implement Transformer analysis
                            Settings.ANALYZED_ARTICLES.add(
                                row.iloc[1]
                            )  # Using int as key is depracated for future use
                else:
                    logger.warning("No valid articles after preprocessing.")
            else:
                logger.info("No new articles. Running transformer on backlog...")
                # TODO: Process backlog or older articles with transformer
        except Exception as e:
            logger.error(f"Main loop error: {e}")
        logger.info("Loop done! Check output for visual representation")
        logger.info("Summaries:")
        output = "\r"
        for summary in summaries:
            output += f"{summary[0]}:\n{summary[1]}\n----------\n"
        print(f"{output}", end="\r")
        time.sleep(60)


if __name__ == "__main__":
    main()
