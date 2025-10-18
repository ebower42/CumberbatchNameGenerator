import random
import json
from pathlib import Path
from typing import Union

PATH_TO_JSON = Path(__file__).parent / "words.json"


class Generator:

  def __init__(self, json_path: Union[Path, str]=PATH_TO_JSON):

    with open(PATH_TO_JSON, 'r') as f:
      word_list = json.load(f)

    self.givenPart1_list = word_list.get("givenPart1", ["Bene"])
    self.givenPart2_list = word_list.get("givenPart2", ["dict"])
    self.surnamePart1_list = word_list.get("surnamePart1", ["Cumber"])
    self.surnamePart2_list = word_list.get("surnamePart2", ["batch"])

    return
  
  def name(self):
    first = random.choice(self.givenPart1_list) + random.choice(self.givenPart2_list)
    last = random.choice(self.surnamePart1_list) + random.choice(self.surnamePart2_list)
    return first.capitalize() + " " + last.capitalize()

if __name__ == "__main__":
    gen = Generator()
    p = Path('~', 'Piper TTS', 'names.txt').expanduser()
    with open(p, 'w') as f:
        for _ in range(100):
            f.write(gen.name() + '.\n')