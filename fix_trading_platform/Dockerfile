FROM continuumio/miniconda3

WORKDIR /app

COPY environment.yml .

# Create the Conda environment
RUN conda env create -f environment.yml

# Updating compilers and linux.
RUN apt-get update && apt-get install -y \
    gcc g++ unixodbc-dev

# The app code
COPY app/ ./app
WORKDIR ./app

EXPOSE 8000

# Run using conda environment
CMD ["conda", "run", "--no-capture-output", "-n", "trading", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
