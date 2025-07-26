# Use Miniconda as base image
FROM continuumio/miniconda3

# Set working directory
WORKDIR /app

# Copy your environment.yml file into the image
COPY environment.yml .

# Create the Conda environment
RUN conda env create -f environment.yml

# Activate the environment for the rest of the image
SHELL ["conda", "run", "--no-capture-output", "-n", "trading", "/bin/bash", "-c"]

# Install system packages and build quickfix from source

#RUN apt-get update && apt-get install -y \
#    build-essential \
#    libboost-all-dev \
#    cmake \
#    git \
# && git clone https://github.com/quickfix/quickfix.git \
# && cd quickfix && ./bootstrap && ./configure && make && make install \
# && cd .. && rm -rf quickfix

# Copy application code
COPY app/ ./app
WORKDIR /app/app

# Run the FastAPI app inside the Conda env
#CMD ["conda", "run", "--no-capture-output", "-n", "trading", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
CMD ["conda", "run", "-n", "trading", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
