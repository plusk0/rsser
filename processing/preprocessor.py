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
    Expects HTML-Formatted Text.
    Returns cleaned plain text.
    """
    if not isinstance(text, str):
        return ""
    try:
        # Remove HTML tags
        soup = BeautifulSoup(text, "html.parser")
        block_tags = [
            "p",
            "div",
            # "li",
            "h1",
            "h2",
            "h3",
            "h4",
            "h5",
            "h6",
            "blockquote",
            "article",
        ]
        title = "Title not found"
        sentences = []
        for tag in block_tags:
            for element in soup.find_all(tag):
                text = element.get_text(
                    " "
                ).strip()  # Space is needed for seperating punctuation from next word
                if text:
                    element_sentences = sent_tokenize(text)
                    sentences.extend(element_sentences)
                    if tag == "h1":
                        title = element.get_text(" ")
        # Fallback: If no block tags found, split the entire text - might contain weird text snippets
        if not sentences:
            text = soup.get_text(" ").strip()
            if text:
                sentences = sent_tokenize(text)

        text = re.sub(r"\s+", " ", text).strip()
        # Remove placeholder text - Yes this is placeholder code
        # text = re.sub(r"Getty Images|Reuters|AP|\([^)]*\)", " ", text)
        return title, text
    except Exception as e:
        logger.error(f"Failed to preprocess text: {e}")
        return "", ""


def preprocess_for_lda(text):
    """
    Word-level preprocessing for LDA.
    Returns a list of tokens.
    """
    title, text = preprocess_text(text)
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
    title, text = preprocess_text(text)
    if not text:
        return "", []

    sentences = sent_tokenize(text)
    return title, [s.strip() for s in sentences if s.strip()]
