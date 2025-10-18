from generator import Generator
import os
import discord
from discord.ext import commands

BOT_DESCRIPTION = "A bot to generate alternate names for Benedict Cumberbatch."
RAW_PREFIX = "!batch"
SPACE_PREFIX = RAW_PREFIX + " "
BOT_TOKEN = os.getenv("BOT_TOKEN")
FFMPEG_EXEC = "C:\\Users\\ebowe\\AppData\\Local\\Microsoft\\WinGet\\Packages\\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\\ffmpeg-8.0-full_build\\bin\\ffmpeg.exe"

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

bot = commands.Bot(command_prefix=SPACE_PREFIX, description=BOT_DESCRIPTION, intents=intents)
name_api = Generator()

g_last_name = "Benedict Cumberbatch"
g_last_phone = "benedict cumberbatch"


def vc_for(guild: discord.Guild) -> discord.VoiceClient | None:
    return discord.utils.get(bot.voice_clients, guild=guild)


async def _gen(ctx: commands.Context):
    global g_last_name, g_last_phone
    name, phone = name_api.name()
    g_last_name = name
    g_last_phone = phone
    await ctx.send(name)



@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} - {bot.user.id}')
    print('------')


@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    if message.content.strip() == RAW_PREFIX:
        ctx = await bot.get_context(message)
        return await _gen(ctx)
    else:
        return await bot.process_commands(message)


@bot.command(name="gen")
async def gen(ctx):
    await _gen(ctx)

@bot.command(name="join")
async def join(ctx: commands.Context):
    if not isinstance(ctx.author, discord.Member):
        return await ctx.reply("Could not resolve your member information.", mention_author=False)
    if not ctx.author.voice or not ctx.author.voice.channel:
        return await ctx.reply("You are not connected to a voice channel.", mention_author=False)
    channel = ctx.author.voice.channel
    vc = vc_for(ctx.guild)
    if vc and vc.is_connected():
        await vc.move_to(channel)
    else:
        await channel.connect()
    return await ctx.reply(f"Joined {channel.name}.", mention_author=False)


@bot.command(name="leave")
async def leave(ctx: commands.Context):
    vc = vc_for(ctx.guild)
    if not vc or not vc.is_connected():
        return await ctx.reply("I am not connected to a voice channel.", mention_author=False)
    await vc.disconnect()
    return await ctx.reply("Disconnected.", mention_author=False)


@bot.command(name="play")
async def play(ctx: commands.Context):
    vc = vc_for(ctx.guild)
    if not vc or not vc.is_connected():
        return await ctx.reply("I am not connected to a voice channel.", mention_author=False)
    if not vc.is_playing():
        name_api.vocalize(g_last_phone)
        vc.play(discord.FFmpegPCMAudio(executable=FFMPEG_EXEC, source="audio/output.wav"))
        return await ctx.reply("Playing audio.", mention_author=False)
    else:
        return await ctx.reply("Audio is already playing.", mention_author=False)


def run(token=BOT_TOKEN):
    print(f"Using token: {token}")
    if token is None:
        raise ValueError("The bot token is None. Please either set the BOT_TOKEN environment variable or pass a token "
                         "directly.")
    bot.run(token)


if __name__ == "__main__":
    run()