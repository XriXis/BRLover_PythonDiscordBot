import asyncio

from async_timeout import timeout
from discord import member, message
from discord.ext import commands

from BRBot import BRBot
from Cogs.PickCog import lstOfCharacters
from Utils.MessageLib import reaction, custom_embed
from Utils.JsonHandler import settings, message_texts


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
        ```ARM
        WARNING: you must have open private chat to take part in draft
        ```
        """
        if self.bot.user != ctx.author:
            match len(ctx.message.mentions):
                case 0:
                    await reaction(ctx, False)
                    await ctx.respond(embed=custom_embed(False, "dr1"))
                    return
                case 1:
                    if ctx.message.mentions[0] != ctx.author:
                        capitan1 = ctx.author
                        capitan2 = ctx.message.mentions[0]
                    else:
                        await reaction(ctx, False)
                        await ctx.respond(embed=custom_embed(False, "dr1"))
                        return
                case 2:
                    capitan1 = ctx.message.mentions[0]
                    capitan2 = ctx.message.mentions[1]

                case _:
                    await reaction(ctx, False)
                    await ctx.respond(embed=custom_embed(False, "dr2"))
                    return
            await reaction(ctx, True)
            ban_list = [[], []]
            order = ["ban", "pick", "pick", "ban", "pick"]
            sentences_for_phases = {
                "ban":
                    message_texts["dr3"],
                "pick":
                    message_texts["dr4"]
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
                    await capitan2.send(embed=custom_embed(True, "dr5", captains_ans[0]))
                    await capitan1.send(embed=custom_embed(True, "dr5", captains_ans[1]))
            except asyncio.TimeoutError:
                await reaction(ctx, False)
                await ctx.respond("Someone is not ready! (time for draft is out)")

    async def choose(self, user: member, ban_list: list[str] = (), *, sentence: str) -> message:
        """
        This function provide one-time choose phase-character for 2 captains, without waiting
        """
        # need to add timeout ending count
        await user.send(embed=custom_embed(True, "ch1", sentence))
        async with timeout(settings["time_to_draft_phase_in_seconds"]):
            while True:
                msg = await self.bot.wait_for("message", check=lambda m: m.author == user)
                ans = msg.content.capitalize()
                if ans == "Characters":
                    for group in lstOfCharacters:
                        await user.send(group + ":\n" + "\n".join(hero for hero in lstOfCharacters[group]),
                                        delete_after=60.0)
                elif ans in ban_list:
                    await user.send(embed=custom_embed(False, "ch2"))
                elif ans in [hero for group in lstOfCharacters for hero in lstOfCharacters[group]]:

                    return ans
                else:
                    await user.send(embed=custom_embed(False, "ch3"))


def setup(bot: BRBot) -> None:
    bot.add_cog(DraftCog(bot))
