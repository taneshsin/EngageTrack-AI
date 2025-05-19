# Base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy files
COPY ./src /app/src
COPY ./data /app/data
COPY ./requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create a non-root user and switch to it
RUN adduser --disabled-password --gecos '' appuser && \
    mkdir -p /app/logs && \
    chown -R appuser /app/logs

# Switch to non-root user
USER appuser

# Run Streamlit app
CMD ["streamlit", "run", "src/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
