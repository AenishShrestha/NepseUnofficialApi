FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Install dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy the application files into the container
COPY . .

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Install gunicorn
RUN pip install gunicorn

# Expose the port that your Flask app will run on
EXPOSE 8007

# Run the application using gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8007", "example.NepseServer:app"]

