
FROM continuumio/miniconda3:latest

# Set the working directory
WORKDIR /app


COPY environment.yml .


RUN conda env create -f environment.yml && \
  conda clean -afy && \
  conda init


COPY . .

# Make RUN commands use the new environment
SHELL ["conda", "run", "-n", "rssenv", "/bin/bash", "-c"]

# Set NLTK_DATA environment variable
ENV NLTK_DATA=/opt/nltk_data


# Create NLTK data directory and download resources
RUN mkdir -p ${NLTK_DATA} && \
  python -c "import nltk; nltk.download('punkt', download_dir='${NLTK_DATA}'); nltk.download('stopwords', download_dir='${NLTK_DATA}'); nltk.download('punkt_tab', download_dir='${NLTK_DATA}')"


# Set environment variables
ENV PYTHONPATH=/app \
  PYTHONUNBUFFERED=1 \
  NLTK_DATA=/opt/nltk_data


CMD ["python", "main.py"]

