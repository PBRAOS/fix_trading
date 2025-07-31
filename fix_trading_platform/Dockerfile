FROM continuumio/miniconda3

WORKDIR /app

COPY environment.yml .

# Create the Conda environment
RUN conda env create -f environment.yml

# Copy your app code
COPY app/ /app/app
WORKDIR /app/app

EXPOSE 8000

# Run using conda environment
CMD ["conda", "run", "--no-capture-output", "-n", "trading", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
