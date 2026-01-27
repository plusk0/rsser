from gensim import corpora, models

# import pyLDAvis.gensim_models as gensimvis
from config.settings import Settings
import logging
import networkx
import itertools
import editdistance

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


# Graph builder for statistical summarizing
def build_graph(nodes):
    """
    Following implementation via Textrank by davidadamojr
    Return a networkx graph instance.

    :param nodes: List of hashables that represent the nodes of a graph.
    """
    try:
        gr = networkx.Graph()  # initialize an undirected graph
        gr.add_nodes_from(nodes)
        nodePairs = list(itertools.combinations(nodes, 2))
        # add edges to the graph (weighted by Levenshtein distance)
        for pair in nodePairs:
            firstString = pair[0]
            secondString = pair[1]
            levDistance = editdistance.eval(firstString, secondString)
            gr.add_edge(firstString, secondString, weight=levDistance)
    except Exception as e:
        logger.error(f"Graph building failed: {e}")
    return gr


def summarize_text(sentence_tokens):
    try:
        summary_length = Settings.user_settings.summary_len
        graph = build_graph(sentence_tokens)

        calculated_page_rank = networkx.pagerank(graph, weight="weight")
        # most important sentences in ascending order of importance
        sentences = sorted(
            calculated_page_rank, key=calculated_page_rank.get, reverse=True
        )
        # return a [X] word summary
        summary = " ".join(sentences)
        summary_words = summary.split()

        # Truncate to summary_length words
        if len(summary_words) > summary_length:
            truncated_words = summary_words[:summary_length]
            # Find the last period in the truncated words
            last_dot_index = -1
            for i, word in enumerate(truncated_words):
                if "." in word:
                    last_dot_index = i
            # If a period is found, truncate at that position + 1 (to include the word with the period)
            if last_dot_index != -1:
                summary = " ".join(truncated_words[: last_dot_index + 1])
            else:
                summary = " ".join(truncated_words)
        else:
            summary = " ".join(summary_words)
    except Exception as e:
        logger.error(f"Summarizing failed: {e}")
        summary = ""
    return summary
