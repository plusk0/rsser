from bs4 import BeautifulSoup
import re
import string
import logging
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords

logger = logging.getLogger(__name__)


def preprocess_for_lda(text):
    """
    Word-level preprocessing for LDA.
    Returns a list of tokens.
    """

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

    if not text:
        return "", []

    sentences = sent_tokenize(text)
    return [s.strip() for s in sentences if s.strip()]
