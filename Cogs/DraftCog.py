from discord import member, Option, Member
from discord.ext import commands

from BRBot import BRBot
from Utils.JsonHandler import settings
from Utils.MessageLib import custom_embed
from Utils.DraftSystem.Draft import Draft


class DraftCog(commands.Cog):
    """
    Now, I really don't know for what I create cog for 1 command, but this command can take dRaFt SyStEm
    """

    def __init__(self, bot: BRBot) -> None:
        self.bot: BRBot = bot

    @commands.has_role(settings["privileged role"])
    @commands.slash_command(name="draft_between", description="start draft between 2 members of your guild")
    async def owner_draft(self, ctx, captain1: Option(Member), captain2: Option(Member)):
        await self.draft(ctx, captain1, captain2)

    @commands.slash_command(name="draft_with", description="you can throw fight to the user")
    async def text_draft(self, ctx, captain: Option(Member)):
        await self.draft(ctx, ctx.author, captain)

    @commands.user_command(name="draft_with", description="you can throw fight to user")
    async def context_draft(self, ctx, captain: member) -> None:
        await self.draft(ctx, ctx.author, captain)

    async def draft(self, ctx, captain1: Member, captain2: Member):
        if captain1 == captain2:
            await ctx.respond(embed=custom_embed(False, "1 capitan in draft"))
        elif any(captain == self.bot.user for captain in (captain1, captain2)):
            await ctx.respond(embed=custom_embed(False, "draft with bot"))
        else:
            await ctx.respond(embed=custom_embed(True, "empty", "👌"))
            draft = Draft(captain1, captain2, ctx.channel)
            await draft.start()


def setup(bot: BRBot) -> None:
    bot.add_cog(DraftCog(bot))
