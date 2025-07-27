# Use Miniconda as base image
FROM continuumio/miniconda3

# Set working directory inside the container
WORKDIR /app

# Copy Conda environment file into the image
COPY environment.yml .

# Create the Conda environment named 'trading'
RUN conda env create -f environment.yml

# List files to confirm build context
RUN echo "📦 Files in /app:" && ls -al /app

# Set shell to use the 'trading' conda environment for all subsequent commands
SHELL ["conda", "run", "--no-capture-output", "-n", "trading", "/bin/bash", "-c"]

# Install system packages and build quickfix from source
RUN apt-get update && apt-get install -y \
    build-essential \
    libboost-all-dev \
    cmake \
    git \
 && git clone https://github.com/quickfix/quickfix.git \
 && cd quickfix  \
 && ./bootstrap  \
 && ./configure  \
 && make && make install \
 && ls \
 && cd .. && rm -rf quickfix \
 ## && pip install quickfix    # Install the package once its built.

# Copy your application code into the container
COPY app/ ./app

# Change working directory to your app code
WORKDIR /app/app

# Expose FastAPI port
EXPOSE 8000

# Launch FastAPI using Uvicorn from within the conda environment
CMD ["conda", "run", "--no-capture-output", "-n", "trading", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
