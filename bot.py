from generator import Generator
import os
import discord
from discord.ext import commands
from typing import Any, Optional
import logging
from pathlib import Path
from eleven_labs_api import ElevenLabsAPI

DEBUG = os.getenv("DEBUG")
AUDIO_DIR = os.getenv("AUDIO_DIR", "/audio")
FFMPEG_EXEC = os.getenv("FFMPEG_EXEC", "ffmpeg")

RAW_PREFIX = "!batch"
RAW_PREFIX_SHORT = "!b"
SPACE_PREFIX = RAW_PREFIX + " "
BOT_TOKEN = os.getenv("BOT_TOKEN")
ELEVEN_LABS_TOKEN = os.getenv("ELEVEN_LABS_TOKEN")
BOT_DESCRIPTION = ("A bot to generate alternate names for Benedict Cumberbatch.\n"
                   "\n"
                   f"Usage: {RAW_PREFIX_SHORT} [command] [arguments]\n"
                   f"\n"
                   f"Running with no command is equivalent to running '{RAW_PREFIX_SHORT} gen'\n")

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True


class CustomHelp(commands.DefaultHelpCommand):
    def get_command_signature(self, command):
        return f"Usage: {super().get_command_signature(command)}"
    def get_ending_note(self):
        return f"Type {RAW_PREFIX_SHORT} [help|?] <command> for more info on a command."
    def add_indented_commands(self, _commands, *, heading, max_size=None):
        max_size = super().get_max_size(_commands) + self.indent
        return super().add_indented_commands(_commands, heading=heading, max_size=max_size)

bot = commands.Bot(
    command_prefix=commands.when_mentioned_or(SPACE_PREFIX, "!b "),
    description=BOT_DESCRIPTION,
    intents=intents,
    help_command=CustomHelp(
        show_parameter_descriptions=False,
        no_category="Commands",
        command_attrs={
            "aliases": ["?"],
            "help": "Get general help information or help about a specific command"
        }
    )
)

name_api = Generator()
eleven_labs_api = ElevenLabsAPI(ELEVEN_LABS_TOKEN)

g_last_name = "Benedict Cumberbatch"
g_last_phone = "benedict cumberbatch"
g_autospeak = False


def vc_for(guild: discord.Guild) -> discord.VoiceClient | None:
    return discord.utils.get(bot.voice_clients, guild=guild)


async def _speak(ctx: commands.Context) -> Optional[Any]:
    global g_autospeak
    vc = vc_for(ctx.guild)
    if not vc or not vc.is_connected():
        return await ctx.reply("I am not connected to a voice channel.", mention_author=False)
    if not vc.is_playing():
        _count = eleven_labs_api.get_remaining_character_count()
        if _count < 20:
            name_api.vocalize(g_last_phone)
            audio_source = Path(AUDIO_DIR) / "output.wav"
        else:
            audio_source = eleven_labs_api.get_spoken_name(g_last_name, AUDIO_DIR)
        return vc.play(discord.FFmpegPCMAudio(executable=FFMPEG_EXEC, source=str(audio_source)))
    else:
        return await ctx.reply("Audio is already playing.", mention_author=False)

async def _gen(ctx: commands.Context):
    global g_last_name, g_last_phone, g_autospeak
    name, phone = name_api.name()
    g_last_name = name
    g_last_phone = phone
    await ctx.reply(name)
    if g_autospeak:
        await _speak(ctx)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} - {bot.user.id}')
    print('------')
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Activity(
            type=discord.ActivityType.custom,
            state=f"Type '{RAW_PREFIX_SHORT} help'",
            name=bot.user.name
        )
    )


@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return
    if message.content.strip() == RAW_PREFIX or message.content.strip() == RAW_PREFIX_SHORT:
        ctx = await bot.get_context(message)
        return await _gen(ctx)
    else:
        return await bot.process_commands(message)

@bot.event
async def on_command(ctx: commands.Context):
    print(f"Command '{ctx.command}' invoked by {ctx.author} in guild '{ctx.guild}' (ID: {ctx.guild.id})")


@bot.event
async def on_command_error(ctx: commands.Context, error: commands.CommandError):
    if isinstance(error, commands.CommandNotFound):
        args = ctx.message.content.split()
        cmd = args[1] if len(args) > 1 else ""
        return await ctx.reply(f"Unknown command: '{cmd}'\nUse '{RAW_PREFIX} help'")
    print(str(error))
    return await ctx.reply(f"An error occurred: {str(error)}", mention_author=False)


@bot.command(name="gen",
             help="Generate a new name. (Hint: You can also just type '!b')")
async def gen(ctx):
    await _gen(ctx)


@bot.command(name="join",
             help="Join the voice channel you are in")
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


@bot.command(name="leave",
             help="Leave the voice channel you are in")
async def leave(ctx: commands.Context):
    global g_autospeak
    vc = vc_for(ctx.guild)
    if not vc or not vc.is_connected():
        return await ctx.reply("I am not connected to a voice channel.", mention_author=False)
    await vc.disconnect()
    g_autospeak = False
    return await ctx.reply("Disconnected.", mention_author=False)


@bot.command(name="speak",
             brief="Speak name in voice channel",
             help="Speak the last generated name in the voice channel.",
             aliases=["say"])
async def speak(ctx: commands.Context):
    await _speak(ctx)


@bot.command(name="autospeak",
             brief="Turn on/off autospeak",
             usage="[on|off]",
             help="Running without arguments turns on autospeak",
             description="If autospeak is on, the bot automatically speaks any generated names",
             aliases=["auto"])
async def autospeak(ctx: commands.Context, subcmd: str = "on"):
    global g_autospeak
    if subcmd == "on":
        g_autospeak = True
        return await ctx.reply(f"Autospeak on")
    else:
        g_autospeak = False
        return await ctx.reply(f"Autospeak off")


# Hidden Commands
@bot.command(name="count",
             hidden=True)
async def count(ctx: commands.Context):
    cnt = eleven_labs_api.get_remaining_character_count()
    return await ctx.reply(f"{cnt} characters")


def run(token=BOT_TOKEN):
    if DEBUG:
        print(f"Using token: {token}")
    if token is None:
        raise ValueError("The bot token is None. Please either set the BOT_TOKEN environment variable or pass a token "
                         "directly.")
    bot.run(token)


if __name__ == "__main__":
    run()