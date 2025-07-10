from generator import Generator
from bot import Bot
import os
from keepAlive import keep_alive

bot = Bot()
t = os.environ['BOT_TOKEN']

keep_alive()
bot.run(t)
