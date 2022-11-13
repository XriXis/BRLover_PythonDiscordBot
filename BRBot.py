import os
import traceback
import discord
from discord import Intents, \
    NoEntryPointError, \
    ExtensionNotFound, \
    ExtensionFailed
from discord.ext.bridge import \
    Bot as BotBase

from CustomHelpCommand import CustomHelpCommand
from Utils.JsonHandler import settings

initial_extensions = [f'Cogs.{x}' for x in [
    "PickCog",
    "VoiceCog",
    "StateCog",
    "DraftCog",
    "AdminCog",
    "Sup"
]]


class BRBot(BotBase):
    def __init__(self):
        intents = Intents.default()
        intents.members = True
        intents.message_content = True
        super().__init__(
            command_prefix=settings['prefix'],
            case_insensitive=False,
            help_command=CustomHelpCommand(),
            intents=intents,
            debug_guilds=settings["guilds"]
        )
        self.bot_version = '0.0.0'

    def load_cogs(self) -> None:
        for ext in initial_extensions:
            try:
                self.load_extension(ext)
            except (
                    ExtensionNotFound,
                    NoEntryPointError,
                    ExtensionFailed,
            ):
                print(f'Failed to load extension {ext}.')
                traceback.print_exc()

    async def change_presence_to_help(self) -> None:
        activity_type = discord.ActivityType.listening
        await self.change_presence(activity=discord.Activity(
            type=activity_type,
            name=f"{settings['prefix']}help "
        ))


def runBRo() -> None:
    bot = BRBot()

    bot.load_cogs()
    bot.run(os.getenv('TOKEN'))
