from elevenlabs.client import ElevenLabs
import os

VOICE = "Clyde"

AUDIO_PATH = "C:\\Users\\ebowe\\Programming\\Python\\CumberbatchNameGenerator\\audio\\eleven.wav"

VOICE_ID_MAP = {
    "Clyde": "wyWA56cQNU2KqUW4eCsI",
    "Charles": "zNsotODqUhvbJ5wMG7Ei"
}

client = ElevenLabs(
    api_key=os.getenv("ELEVEN_LABS_API_KEY"),
)

audio = client.text_to_speech.convert(
    text="Babydust Supperrap",
    voice_id=VOICE_ID_MAP[VOICE],
    model_id="eleven_turbo_v2_5"

)