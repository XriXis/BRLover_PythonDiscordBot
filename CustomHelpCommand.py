from discord import Embed
from discord.ext import commands
from discord.colour import Colour

from SystemsRealisations.JsonHandler import settings, message_texts


class CustomHelpCommand(commands.HelpCommand):
    def __init__(self):
        super().__init__()

    lang = message_texts['help']

    async def send_bot_help(self, mapping):
        embed = Embed(title="Help", colour=Colour.red())

        for cog, lst_of_commands in mapping.items():
            for command in lst_of_commands:
                embed.add_field(name=f"{settings['prefix']}{command.name}", value=self.lang[command.name], inline=False)
        channel = self.get_destination()
        await channel.send(embed=embed)

    async def send_command_help(self, command):
        embed = Embed(title="Command help", colour=Colour.red())
        embed.add_field(name=f"{settings['prefix']}{command.name}", value=self.lang[command.name])
        channel = self.get_destination()
        await channel.send(embed=embed)
