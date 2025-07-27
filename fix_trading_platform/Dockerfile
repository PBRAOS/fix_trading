FROM continuumio/miniconda3

WORKDIR /app

COPY environment.yml .

# Create the Conda environment
RUN conda env create -f environment.yml

# Install system packages (not inside conda env!)
RUN apt-get update && apt-get install -y \
    build-essential \
    libboost-all-dev \
    cmake \
    git \
    libtool \
    autoconf \
    automake \
    swig

# Clone and build QuickFIX
RUN git clone https://github.com/quickfix/quickfix.git && \
    cd quickfix && \
    ./bootstrap && \
    ./configure --with-python && \
    make -j2 && \
    make install && \
    cd python && \
    conda run -n trading python setup.py install

# Copy your app code
COPY app/ /app/app
WORKDIR /app/app

EXPOSE 8000

# Run using conda environment
CMD ["conda", "run", "--no-capture-output", "-n", "trading", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
