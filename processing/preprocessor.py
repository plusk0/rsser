import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
import logging

logger = logging.getLogger(__name__)


def preprocess(text):
    if not isinstance(text, str):
        return []
    try:
        text = text.lower()
        text = text.translate(str.maketrans("", "", string.punctuation))
        tokens = word_tokenize(text)
        return [
            word
            for word in tokens
            if word not in stopwords.words("english") and len(word) > 2
        ]
    except Exception as e:
        logger.error(f"Failed to preprocess text: {e}")
        return []
