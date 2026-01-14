
FROM continuumio/miniconda3:latest

# Set the working directory
WORKDIR /app


COPY environment.yml .


RUN conda env create -f environment.yml && \
  conda clean -afy


COPY . .

# Make RUN commands use the new environment
SHELL ["conda", "run", "-n", "rssenv", "/bin/bash", "-c"]


CMD ["python", "main.py"]

