from transformers import pipeline
import logging

logger = logging.getLogger(__name__)

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")


def summarize(text):
    try:
        return summarizer(text, max_length=130, min_length=30, do_sample=False)[0][
            "summary_text"
        ]
    except Exception as e:
        logger.error(f"Transformer summarization failed: {e}")
        return None
