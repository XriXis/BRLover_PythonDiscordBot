from discord import member
from discord.ext import commands

from BRBot import BRBot
from Utils.MessageLib import custom_embed
from Utils.DraftSystem.Draft import Draft


class DraftCog(commands.Cog):
    """
    Now, I really don't know for what I create cog for 1 command, but this command can take dRaFt SyStEm
    """

    def __init__(self, bot: BRBot) -> None:
        self.bot: BRBot = bot

    @commands.user_command(name="draft with", description="you can throw fight to user")
    async def draft(self, ctx, captain: member) -> None:
        if captain == ctx.author:
            await ctx.respond(embed=custom_embed(False, "1 capitan in draft"))
        elif captain == self.bot.user:
            await ctx.respond(embed=custom_embed(False, "draft with bot"))
        else:
            await ctx.respond(embed=custom_embed(True, "empty", "👌"))
            draft = Draft(ctx.author, captain, ctx.channel)
            await draft.start()


def setup(bot: BRBot) -> None:
    bot.add_cog(DraftCog(bot))
