# Dockerfile
FROM python:3.13-slim

LABEL maintainer="Eric Bower"

ENV APP_ROOT=/app
ENV PIPER_VOICES_DIR=/voices
ENV LOG_DIR=/log
ENV AUDIO_DIR=/audio
ENV PIPER_VOICE=en_GB-alan-medium
ENV PYTHONUNBUFFERED=1

ARG IMAGE_VERSION
ENV IMAGE_VERSION=${IMAGE_VERSION}

# Create necessary directories
RUN mkdir -p ${APP_ROOT} ${LOG_DIR} ${AUDIO_DIR} ${PIPER_VOICES_DIR}

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg libopus0 libsodium23 ca-certificates curl espeak \
    && rm -rf /var/lib/apt/lists/*

# Copy bot source code
COPY ./src/* ${APP_ROOT}/
COPY requirements.txt ${APP_ROOT}/
COPY LICENSE ${APP_ROOT}/

WORKDIR ${APP_ROOT}

# Install any needed packages
RUN pip install --no-cache-dir -r requirements.txt

# Add entrypoint
COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Create a non-root user
RUN useradd -m botuser

RUN chown -R botuser:botuser ${APP_ROOT} ${LOG_DIR} ${AUDIO_DIR} ${PIPER_VOICES_DIR}

# Use the non-root user
USER botuser

ENTRYPOINT ["docker-entrypoint.sh"]
# Run your bot
CMD ["python", "bot.py"]
