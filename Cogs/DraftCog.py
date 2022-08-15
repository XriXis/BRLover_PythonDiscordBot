import asyncio

from async_timeout import timeout
from discord import member, message
from discord.ext import commands

from BRBot import BRBot
from Cogs.PickCog import lstOfCharacters
from Utils.MessageLib import reaction
from Utils.JsonHandler import settings


class DraftCog(commands.Cog):
    """
    Now, I really don't know for what I create cog for 1 command, but this command can take dRaFt SyStEm
    """

    def __init__(self, bot: BRBot) -> None:
        self.bot: BRBot = bot

    @commands.command()
    @commands.has_role(settings["privileged role"])
    async def draft(self, ctx) -> None:
        # test with anyone
        """
        This command realise draft system, now it works like awaitable private chat, so you can run into some troubles
        with right writing of characters names, so it solves with another command in hidden text in messages to you,
        that give you all correctly english names of characters (just copy hidden text and paste it in private chat)
        ||But in plans to make it look like this: https://brdraft.com/||
        ```
        WARNING: you must have open private chat to take part in draft
        ```
        """
        if self.bot.user != ctx.author:
            match len(ctx.message.mentions):
                case 0:
                    await reaction(ctx, False)
                    await ctx.reply("You ment lesser people than needier. Call one (if YOU play in next clutch)"
                                    " or two team captains")
                    return
                case 1:
                    capitan1 = ctx.author
                    capitan2 = ctx.message.mentions[0]
                case 2:
                    capitan1 = ctx.message.mentions[0]
                    capitan2 = ctx.message.mentions[1]

                case _:
                    await reaction(ctx, False)
                    await ctx.reply("You ment more people than needier. Call only the (two) team captains, "
                                    "or (if you one of them) another one capitan")
                    return
            await reaction(ctx, True)
            ban_list = [[], []]
            order = ["ban", "pick", "pick", "ban", "pick"]
            sentences_for_phases = {
                "ban":
                    "Choose hero what you want to ban for enemy team.",
                "pick":
                    "Choose hero what you want to add in your command."
            }
            try:
                for phase in order:
                    sentence = sentences_for_phases[phase]
                    captains_ans = await asyncio.gather(
                        self.choose(capitan1, ban_list[1], sentence=sentence),
                        self.choose(capitan2, ban_list[0], sentence=sentence)
                    )
                    if phase == "ban":
                        ban_list[0] += [captains_ans[0]]
                        ban_list[1] += [captains_ans[1]]
                    await capitan2.send(f"Your opponent chose {captains_ans[0]} in there phase.")
                    await capitan1.reply(f"Your opponent chose {captains_ans[1]} in there phase.")
            except asyncio.TimeoutError:
                await reaction(ctx, False)
                await ctx.reply("Someone is not ready! (time for draft is out)")

    async def choose(self, user: member, ban_list: list[str] = (), *, sentence: str) -> message:
        """
        This function provide one-time choose phase-character for 2 captains, without waiting
        """
        # need to add timeout ending count
        await user.send(f"{sentence} ~~keyword~~: ||Characters||")
        async with timeout(settings["time_to_draft_phase_in_seconds"]):
            while True:
                msg = await self.bot.wait_for("message", check=lambda m: m.author == user)
                ans = msg.content.capitalize()
                if ans == "Characters":
                    for group in lstOfCharacters:
                        await user.send(group + ":\n" + "\n".join(hero for hero in lstOfCharacters[group]),
                                        delete_after=60.0)
                elif ans in ban_list:
                    await user.send("Your opponent ban this hero. Are you remember?!")
                elif ans in [hero for group in lstOfCharacters for hero in lstOfCharacters[group]]:

                    return ans
                else:
                    await user.send("Unknown character. Send new! (for see correct names write me **Characters**)")


def setup(bot: BRBot) -> None:
    bot.add_cog(DraftCog(bot))
