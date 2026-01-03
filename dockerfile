# Use lightweight Python image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Install system dependencies (optional but safe)
# RUN apt-get update && apt-get install -y \
#     sqlite3 \
#     && rm -rf /var/lib/apt/lists/*

# Copy application files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir flask

# Expose Flask port
EXPOSE 5000

# Initialize database (safe if already exists)
# RUN python init_db.py

# Run the Flask app
CMD ["python", "app.py"]
