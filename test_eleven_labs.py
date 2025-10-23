from elevenlabs.client import ElevenLabs
from elevenlabs.types import VoiceSettings
import os

VOICE = "Charles"

AUDIO_PATH_WIN = ("C:\\Users\\ebowe\\Programming\\Python\\CumberbatchNameGenerator\\audio\\eleven"
                 ".mp3")
AUDIO_PATH_MAC = "/Users/ebower/workspace/Personal/CumberbatchNameGeneratorBot/audio/eleven.mp3"

VOICE_ID_MAP = {
    "Clyde": "wyWA56cQNU2KqUW4eCsI",
    "Charles": "zNsotODqUhvbJ5wMG7Ei"
}

client = ElevenLabs(
    api_key=os.getenv("ELEVEN_LABS_API_KEY"),
)


def main():
    global client
    voice_settings = VoiceSettings(speed=1.0)

    audio_stream = client.text_to_speech.convert(
        text="Babydust Supperrap",
        voice_id=VOICE_ID_MAP[VOICE],
        model_id="eleven_turbo_v2_5",
        output_format="mp3_44100_128",
        voice_settings=voice_settings,
    )

    with open(AUDIO_PATH_MAC, "wb") as audio_file:
        for chunk in audio_stream:
            audio_file.write(chunk)


def print_credits_usage():
    global client
    subscription = client.user.subscription.get()
    print(f"{subscription.character_count=}")


if __name__ == '__main__':
    print_credits_usage()