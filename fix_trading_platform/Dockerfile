# Use Miniconda as base image
FROM continuumio/miniconda3

# Set working directory inside the container
WORKDIR /app

# Copy Conda environment file into the image
COPY environment.yml .

# Create the Conda environment named 'trading'
RUN conda env create -f environment.yml

# List files to confirm build context
RUN echo "Files in /app:" && ls -al /app

# Use the 'trading' env for everything after this
SHELL ["conda", "run", "--no-capture-output", "-n", "trading", "/bin/bash", "-c"]

# Now install QuickFIX from source (in conda env context)
RUN apt-get update && apt-get install -y \
    build-essential \
    libboost-all-dev \
    cmake \
    git \
    libtool \
    autoconf \
    automake \
    swig \
 && git clone https://github.com/quickfix/quickfix.git \
 && cd quickfix \
 && ./bootstrap \
 && ./configure --with-python \
 && make -j$(nproc) \
 && make install \
 && cd python \
 && python setup.py install

# Copy your application code into the container
COPY app/ ./app

# Change working directory to your app code
WORKDIR /app/app

# Expose FastAPI port
EXPOSE 8000

# Launch FastAPI using Uvicorn from within the conda environment
CMD ["conda", "run", "--no-capture-output", "-n", "trading", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
