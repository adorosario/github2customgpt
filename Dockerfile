FROM python:3.11-slim

WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies and wget for healthcheck
RUN apt-get update && \
    apt-get install -y wget && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose the port Streamlit runs on
EXPOSE 8501

# Create a non-root user and switch to it
RUN useradd -m -r streamlit && \
    chown -R streamlit:streamlit /app
USER streamlit

# Command to run the application
CMD ["streamlit", "run", "github_sitemap_generator.py", "--server.address=0.0.0.0"]