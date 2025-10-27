import random
import json
from pathlib import Path
from typing import Union, Optional
from piper import PiperVoice
import wave
from user_settings import PIPER_VOICE_ID, PIPER_VOICES_DIR, AUDIO_DIR
from eleven_labs_api import ElevenLabsAPI

PATH_TO_JSON = Path(__file__).parent / "phonemized_words.json"
VOICE_FILE = Path(PIPER_VOICES_DIR) / f"{PIPER_VOICE_ID}.onnx"
VOICE = PiperVoice.load(VOICE_FILE)


class Generator:
    def __init__(self, json_path: Union[Path, str]=PATH_TO_JSON, eleven_labs_api_token: Optional[str] = None):
        with open(str(json_path), 'r') as f:
          word_list = json.load(f)

        self.givenPart1_map = word_list.get("givenPart1", {"Bene": "bene"})
        self.givenPart2_map = word_list.get("givenPart2", {"dict": "dict"})
        self.surnamePart1_map = word_list.get("surnamePart1", {"Cumber": "cumber"})
        self.surnamePart2_map = word_list.get("surnamePart2", {"batch": "batch"})

        if eleven_labs_api_token is not None:
            self.eleven_labs_api = ElevenLabsAPI(eleven_labs_api_token)
        else:
            self.eleven_labs_api = None
        return
  
    def new_name(self):
        first_part_1 = random.choice(list(self.givenPart1_map.keys()))
        first_part_2 = random.choice(list(self.givenPart2_map.keys()))
        last_part_1 = random.choice(list(self.surnamePart1_map.keys()))
        last_part_2 = random.choice(list(self.surnamePart2_map.keys()))
        first_phone_part_1 = self.givenPart1_map[first_part_1]
        first_phone_part_2 = self.givenPart2_map[first_part_2]
        last_phone_part_1 = self.surnamePart1_map[last_part_1]
        last_phone_part_2 = self.surnamePart2_map[last_part_2]
        first = first_part_1 + first_part_2
        last = last_part_1 + last_part_2
        phone = first_phone_part_1 + first_phone_part_2 + " " + last_phone_part_1 + last_phone_part_2
        return first.capitalize() + " " + last.capitalize(), phone

    def speak(self, name: str, phone: Optional[str] = None) -> Path:
        cnt = 0 if self.eleven_labs_api is None else self.eleven_labs_api.remaining_character_count
        if cnt < 20:
            phone = f"[[ {phone} ]]" if phone else name
            audio_file = Path(AUDIO_DIR) / f"output.wav"
            with wave.open(str(audio_file), 'wb') as output:
                VOICE.synthesize_wav(phone, output)
        else:
            audio_file = self.eleven_labs_api.get_spoken_name(name, AUDIO_DIR)

        return audio_file

    def get_remaining_eleven_labs_character_count(self):
        return 0 if self.eleven_labs_api is None else self.eleven_labs_api.remaining_character_count


def main():
    gen = Generator()
    p = Path('~', 'Piper TTS', 'names.txt').expanduser()
    with open(p, 'w') as f:
        for _ in range(100):
            f.write(gen.new_name()[0] + '.\n')

if __name__ == "__main__":
    main()