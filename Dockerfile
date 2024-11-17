FROM python:3.9-slim

WORKDIR /app

# Install dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create and copy requirements.txt
RUN echo "fastapi==0.78.0\nuvicorn==0.17.6\nrequests==2.31.0\nbeautifulsoup4==4.12.0\npandas==2.0.0\npython-dateutil==2.8.2\naiohttp==3.8.5" > requirements.txt

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Set the port
ENV PORT=8007

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8007"]
