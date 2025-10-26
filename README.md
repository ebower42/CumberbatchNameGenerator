# Cumberbatch Name Generator Discord Bot

![](./image/bandycoot_cumberbund.jpg)

A self-hosted discord bot that randomly generates alternative names to Benedict Cumberbatch, and can even speak them 
in voice chat too!

---

## Features
- **Name Generation** by randomly selecting name parts from a json file
- **Text-to-Speech** using [ElevenLabs](https://elevenlabs.io/) and [Piper TTS](https://github.com/rhasspy/piper)
- **Docker-ready** with configurable env vars and volume mounts

---

## Quick Start (Docker Compose)
Create a `.env` file next to your `docker-compose.yml`:
```dotenv
BOT_TOKEN=your_discord_bot_token
ELEVEN_LABS_TOKEN=your_eleven_labs_api_key
```
Example `docker-compose.yml`
```yaml
services:
  bot:
    image: ghcr.io/ebower42/cumberbatch-name-generator:latest
    restart: unless-stopped
    env_file:
      - .env
    volumes:
      - ./voices:/voices
      - ./audio:/audio
```
Start the bot:
```bash
docker compose up -d
```