import matplotlib.pyplot as plt
import os
import logging
from config.settings import Settings
import pyLDAvis.gensim_models as gensimvis
import pyLDAvis

logger = logging.getLogger(__name__)


def compare_summaries(original, statistical_summary, transformer_summary):
    try:
        plt.figure(figsize=(10, 4))
        plt.title("Summary Comparison")
        plt.text(0.1, 0.8, f"Original: {original[:100]}...")
        plt.text(0.1, 0.5, f"Statistical: {statistical_summary[:100]}...")
        plt.text(0.1, 0.2, f"Transformer: {transformer_summary[:100]}...")
        output_path = os.path.join(Settings.OUTPUT_DIR, "summary_comparison.png")
        plt.savefig(output_path)
        return output_path
    except Exception as e:
        logger.error(f"Summary visualization failed: {e}")
        return None


def visualize_lda(lda, corpus, dictionary):
    try:
        vis = gensimvis.prepare(lda, corpus, dictionary)
        output_path = os.path.join(Settings.OUTPUT_DIR, "lda_visualization.html")
        os.makedirs(Settings.OUTPUT_DIR, exist_ok=True)
        pyLDAvis.save_html(vis, output_path)
        return output_path
    except Exception as e:
        logger.error(f"LDA visualization failed: {e}")
        return None
