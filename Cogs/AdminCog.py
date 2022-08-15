from discord.ext import commands

from BRBot import BRBot
from Utils.MessageLib import reaction
from Utils.JsonHandler import change_prefix_in_data, settings


class AdminCog(commands.Cog):
    """
    This cog for administrate the bot or administrate the guild using bots hands.
    """

    def __init__(self, bot: BRBot) -> None:
        self.bot: BRBot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence_to_help()

    @commands.command()
    @commands.has_role(settings["privileged role"])
    async def change_prefix(self, ctx, newPrefix: str = None, *args):
        """
        Action of this command are locates in their name.
        """
        if ctx.author != self.bot.user:
            if newPrefix is None:
                await reaction(ctx, False)
                await ctx.reply("You must give new prefix to change old!")
            elif newPrefix == "/":
                await reaction(ctx, False)
                await ctx.reply("This is application command prefix, " +
                                "you already can use it to interact with most of bots")
            elif args:
                await reaction(ctx, False)
                await ctx.reply("New prefix mustn't include spaces!")
            else:
                await reaction(ctx, True)
                change_prefix_in_data(newPrefix)
                self.bot.command_prefix = newPrefix
                await self.bot.change_presence_to_help()

    # TO DO: listener of connection, that add new guild to "settings". This needier for auto-location
    # system and slash-commands


def setup(bot: BRBot) -> None:
    bot.add_cog(AdminCog(bot))
