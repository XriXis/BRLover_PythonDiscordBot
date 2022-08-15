from discord.ext import commands


class CustomHelpCommand(commands.HelpCommand):
    def __init__(self):
        super().__init__()
        # TO DO: this
