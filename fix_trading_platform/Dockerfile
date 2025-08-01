FROM continuumio/miniconda3

WORKDIR /app

COPY environment.yml .

# Create the Conda environment
RUN conda env create -f environment.yml

# Install ODBC driver and pyodbc dependencies
RUN apt-get update && apt-get install -y \
    gnupg \
    curl \
    unixodbc-dev \
    gcc \
    g++ \
    libpq-dev \
    libcurl4-openssl-dev \
    # Add Microsoft repository for SQL Server ODBC driver
    && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql17

# Copy your app code
COPY app/ ./app
WORKDIR ./app

EXPOSE 8000

# Run using conda environment
CMD ["conda", "run", "--no-capture-output", "-n", "trading", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
