from elevenlabs.client import ElevenLabs
from elevenlabs.types import VoiceSettings
from dataclasses import dataclass
from pathlib import Path
from typing import Union
from user_settings import ELEVEN_LABS_VOICE_ID

MODEL_ID = "eleven_turbo_v2_5"
OUTPUT_FORMAT = "mp3_44100_128"
CHARLES_VOICE_ID = "zNsotODqUhvbJ5wMG7Ei"


class ElevenLabsAPI:
    def __init__(self, token: str):
        self.client = ElevenLabs(api_key=token)
        self.character_count = 0
        self.character_limit = 0
        self.remaining_character_count = 0
        self.update_character_count()

    def get_spoken_name(self, name: str, audio_dir: Union[Path, str],
                        voice_id: str = ELEVEN_LABS_VOICE_ID, speed: float = 1.0,
                        regen: bool = False) -> Path:
        name_id = name.replace(" ", "_")
        file = Path(audio_dir) / f"{name_id}.mp3"
        if file.exists() and not regen:
            return file

        voice_settings = VoiceSettings(speed=speed)
        audio_stream = self.client.text_to_speech.convert(
            text=name,
            voice_id=voice_id,
            model_id=MODEL_ID,
            output_format=OUTPUT_FORMAT,
            voice_settings=voice_settings
        )
        with open(file, "wb") as f:
            for chunk in audio_stream:
                f.write(chunk)

        self.update_character_count()
        return file

    def update_character_count(self):
        subscription = self.client.user.subscription.get()
        self.character_count = subscription.character_count
        self.character_limit = subscription.character_limit
        self.remaining_character_count = self.character_limit - self.character_count