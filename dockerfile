# Dockerfile

FROM python:3.13-slim

# Create a non-root user
RUN useradd -m botuser

# Install any needed packages
WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your bot source code
COPY . .

# Use the non-root user
USER botuser
  
# Run your bot
CMD ["python", "bot.py"]
