FROM python:3.9-slim

# Install system dependencies for FFmpeg (Audio/Video codecs)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    imagemagick \
    fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

# Configure ImageMagick policy to allow text
RUN sed -i 's/none/read,write/g' /etc/ImageMagick*/policy.xml

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]