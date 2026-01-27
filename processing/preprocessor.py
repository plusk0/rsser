from bs4 import BeautifulSoup
import re
import string
import logging
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords

logger = logging.getLogger(__name__)


def preprocess_text(text):
    """
    Unified preprocessing for both LDA and TextRank.
    Returns cleaned plain text.
    """
    if not isinstance(text, str):
        return ""

    try:
        # Remove HTML tags, seperate by space
        text = BeautifulSoup(text, "html.parser").get_text(" ")
        # Normalize whitespace
        text = re.sub(r"\s+", " ", text).strip()
        # Remove placeholder text - Yes this is placeholder code
        text = re.sub(r"Getty Images|Reuters|AP|\([^)]*\)", " ", text)
        return text
    except Exception as e:
        logger.error(f"Failed to preprocess text: {e}")
        return ""


def preprocess_for_lda(text):
    """
    Word-level preprocessing for LDA.
    Returns a list of tokens.
    """
    text = preprocess_text(text)
    if not text:
        return []

    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    tokens = word_tokenize(text)
    return [
        word
        for word in tokens
        if word not in stopwords.words("english") and len(word) > 2
    ]


def preprocess_for_textrank(text):
    """
    Sentence-level preprocessing for TextRank.
    Returns a list of sentences.
    """
    text = preprocess_text(text)
    if not text:
        return []

    sentences = sent_tokenize(text)
    return [s.strip() for s in sentences if s.strip()]
