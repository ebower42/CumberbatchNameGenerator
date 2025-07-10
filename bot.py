from generator import Generator
import os
import discord


class Bot(discord.Client):

  def __init__(self):
    super().__init__()
    self.api = Generator()
    self.TOKEN = os.environ['BOT_TOKEN']
    
    return

  async def on_ready(self):
    print('Logged on as {0}!'.format(self.user))
    return
  
  async def on_message(self, message):

    if(message.author == self.user):
      return
    
    if(message.content.startswith("!batch")):

      name = self.api.name()

      await message.channel.send(name)
      pass

    return