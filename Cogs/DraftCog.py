from discord import member
from discord.ext import commands

from BRBot import BRBot
from Utils.MessageLib import custom_embed
from Utils.JsonHandler import settings
from Utils.Ui.Draft import Draft


class DraftCog(commands.Cog):
    """
    Now, I really don't know for what I create cog for 1 command, but this command can take dRaFt SyStEm
    """

    def __init__(self, bot: BRBot) -> None:
        self.bot: BRBot = bot

    @commands.user_command(name="draft with", description="you can throw fight to user")
    @commands.has_role(settings["privileged role"])
    async def draft(self, ctx, captain: member) -> None:
        """
        This command implements self system, now it works like awaitable private chat, so you can run into some troubles
        with right writing of characters names, so it solves with another command in hidden text in messages to you,
        that give you all correctly english names of characters (just copy hidden text and paste it in private chat)
        ||But in plans to make it look like this: https://brdraft.com/||
        ```ARM
        WARNING: you must have open private chat to take part in self
        ```
        """
        await ctx.respond(embed=custom_embed(True, "empty", "👌"))
        draft = Draft(ctx.author, captain, ctx.channel)
        await draft.send_start_of_draft_phase()


def setup(bot: BRBot) -> None:
    bot.add_cog(DraftCog(bot))
