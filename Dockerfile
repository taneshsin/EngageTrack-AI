# Base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy files
COPY ./src /app/src
COPY ./data /app/data
COPY ./logs /app/logs
COPY ./requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run Streamlit app
CMD ["streamlit", "run", "src/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
