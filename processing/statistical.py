from gensim import corpora, models
# import pyLDAvis.gensim_models as gensimvis

import logging
# from config.settings import Settings


logger = logging.getLogger(__name__)


def analyze_lda(texts):
    try:
        dictionary = corpora.Dictionary(texts)
        corpus = [dictionary.doc2bow(text) for text in texts]
        lda = models.LdaModel(
            corpus, num_topics=5, id2word=dictionary, passes=10, random_state=42
        )
        return lda, corpus, dictionary
    except Exception as e:
        logger.error(f"LDA analysis failed: {e}")
        return None, None, None
