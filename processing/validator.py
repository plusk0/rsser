from processing.statistical import preprocess
from collections import Counter
import logging

logger = logging.getLogger(__name__)


def validate_summary(original_text, summary):
    try:
        original_keywords = set(preprocess(original_text))
        summary_keywords = set(preprocess(summary))
        overlap = original_keywords.intersection(summary_keywords)
        return len(overlap) / len(summary_keywords) > 0.5  # At least 50% overlap
    except Exception as e:
        logger.error(f"Validation failed: {e}")
        return False
