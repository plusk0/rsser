# Stage 1: Build environment with Miniconda
FROM continuumio/miniconda3:latest AS builder

WORKDIR /app

# Copy the environment.yml file
COPY environment.yml .

# Create the Conda environment from the file
RUN conda env create -f environment.yml

# Make RUN commands use the new environment
SHELL ["conda", "run", "-n", "your_env_name", "/bin/bash", "-c"]

# Copy your script
COPY main.py .

# Stage 2: Runtime environment
FROM continuumio/miniconda3:latest

WORKDIR /app

# Copy the Conda environment from the builder
COPY --from=builder /opt/conda/envs/your_env_name /opt/conda/envs/your_env_name

# Copy your script
COPY main.py .

# Make RUN commands use the new environment
SHELL ["conda", "run", "-n", "your_env_name", "/bin/bash", "-c"]

# Set environment variables
ENV PYTHONPATH=/app \
  PYTHONUNBUFFERED=1

CMD ["python", "main.py"]
