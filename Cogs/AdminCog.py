from discord.ext import commands

from BRBot import BRBot
from Utils.MessageLib import reaction, custom_embed
from Utils.JsonHandler import change_prefix_in_data, settings, change_lang_in_data


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
        if ctx.author != self.bot.user:
            if newPrefix is None:
                await reaction(ctx, False)
                await ctx.respond(embed=custom_embed("chp1"))
            elif newPrefix == "/":
                await reaction(ctx, False)
                await ctx.respond(embed=custom_embed("chp2"))
            elif args:
                await reaction(ctx, False)
                await ctx.respond(embed=custom_embed("chp3"))
            else:
                await reaction(ctx, True)
                change_prefix_in_data(newPrefix)
                self.bot.command_prefix = newPrefix
                await self.bot.change_presence_to_help()

    @commands.command()
    @commands.has_role(settings["privileged role"])
    async def change_language(self, ctx, lang):
        if lang not in settings["support_languages"]:
            await reaction(ctx, False)
            await ctx.respond(embed=custom_embed("chl1", ", ".join(settings["support_languages"])))
        else:
            await reaction(ctx, True)
            change_lang_in_data(lang)
            await ctx.respond(embed=custom_embed("chl2"))

    # TO DO: listener of connection, that add new guild to "settings". This needier for slash-commands


def setup(bot: BRBot) -> None:
    bot.add_cog(AdminCog(bot))
