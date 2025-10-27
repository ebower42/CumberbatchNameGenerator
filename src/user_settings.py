import os

# Tokens
BOT_TOKEN = os.getenv("BOT_TOKEN")
ELEVEN_LABS_TOKEN = os.getenv("ELEVEN_LABS_TOKEN")

# Voice synthesis
AUDIO_DIR = os.getenv("AUDIO_DIR", "/audio")
FFMPEG_EXEC = os.getenv("FFMPEG_EXEC", "ffmpeg")

# Piper
PIPER_VOICE_ID = os.getenv("PIPER_VOICE_ID", "en_GB-alan-medium")
PIPER_VOICES_DIR = os.getenv("PIPER_VOICES_DIR", "/voices")

# ElevenLabs
MAX_ELEVEN_LABS_CHARACTERS = int(os.getenv("MAX_ELEVEN_LABS_CHARACTERS", 10000))
ELEVEN_LABS_VOICE_ID = (os.getenv("ELEVEN_LABS_VOICE_ID", "zNsotODqUhvbJ5wMG7Ei"))

# Discord
AUTO_VOICE_LEAVE_DELAY = int(os.getenv("AUTO_VOICE_LEAVE_DELAY", 20))

# Dev
DEBUG = os.getenv("DEBUG")
