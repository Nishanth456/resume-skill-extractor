# Use a specific, stable, and lightweight Python 3.10 base image
FROM python:3.10-slim-buster

# Set the working directory inside the container
WORKDIR /app

# Install system-level build dependencies required for blis and spaCy
RUN apt-get update && apt-get install -y \
    build-essential \
    libatlas-base-dev \
    gfortran \
    python3-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set CPU flags to avoid architecture-specific blis issues
ENV CFLAGS="-march=core2"

# Set GEMINI API Key as an environment variable
ENV GEMINI_API_KEY="your-api-key-here"

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    python -m spacy download en_core_web_sm

# Create a writable directory for resume data
RUN mkdir -p resumes_data && chmod -R 777 resumes_data

# Copy application files
COPY app.py .
COPY pdf_parser.py .
COPY llm_extractor.py .

# Expose Streamlit's default port
EXPOSE 8501

# Run the Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
