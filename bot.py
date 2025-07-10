from generator import Generator
import os
import discord
from discord.ext import commands

description = "A bot to generate alternate names for Benedict Cumberbatch."

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

bot = commands.Bot(command_prefix='!', description=description, intents=intents)
name_api = Generator()

BOT_TOKEN = os.getenv("BOT_TOKEN")

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} - {bot.user.id}')
    print('------')


@bot.command(name='batch')
async def batch(ctx):
    name = name_api.name()
    await ctx.send(name)


def run(token=BOT_TOKEN):
    print(f"Using token: {token}")
    if token is None:
        raise ValueError("The bot token is None. Please either set the BOT_TOKEN environment variable or pass a token "
                         "directly.")
    bot.run(token)


if __name__ == "__main__":
    run()