import random
import json

class Generator:

  def __init__(self):

    self.defaultWords = {
      "givenPart1": ["bene"],
      "givenPart2": ["dict"],
      "surnamePart1": ["cumber"],
      "surnamePart2": ["batch"]
    }

    return
  
  def name(self):
    first = ""
    last = ""

    try:

      f = open("words.json")
      wordList = json.load(f)
    except Exception as e:
      print("The following error occured: ", e)
      wordList = self.defaultWords
      return "Unable to open word file, please look in the logs on repl.it"
    

    first = random.choice(wordList["givenPart1"]) + random.choice(wordList["givenPart2"])

    last = random.choice(wordList["surnamePart1"]) + random.choice(wordList["surnamePart2"])

    return first.capitalize() + " " + last.capitalize()