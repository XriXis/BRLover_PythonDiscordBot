from async_timeout import timeout
from discord.ext import commands

from BRBot import BRBot
from Utils.MessageLib import reaction, custom_embed
from Utils.HiddenLeague import balance, convert
from Utils.JsonHandler import settings


class VoiceCog(commands.Cog):
    """
    This cog includes commands that must have permission to work with voice channels
    """

    def __init__(self, bot: BRBot) -> None:
        self.bot: BRBot = bot

    @commands.command()
    @commands.has_role(settings["privileged role"])
    async def move_us(self, ctx, *args):
        """
        This command automaticity deliver you and all members of your voice channel to another empty bigger chanel
        """
        if ctx.author != self.bot.user:
            if ctx.author.voice is None:
                await reaction(ctx, False)
                await ctx.respond(embed=custom_embed("mu1"))
            else:
                ok = False
                for channelTo in ctx.guild.voice_channels:
                    if (ctx.author.voice.channel.user_limit < channelTo.user_limit or channelTo.user_limit == 0) \
                            and (len(channelTo.members) < 2):
                        ok = True
                        break
                if not ok:
                    await reaction(ctx, False)
                    await ctx.respond(embed=custom_embed("mu2"))
                elif channelTo == ctx.author.voice.channel:
                    await reaction(ctx, False)
                    await ctx.respond(embed=custom_embed("mu3"))
                else:
                    await reaction(ctx, True)
                    for member in ctx.author.voice.channel.members:
                        await member.move_to(channelTo)
                    await ctx.respond(embed=custom_embed("mu4"))

    # ПРОТЕСТИРУЙ БЛУАУАУА
    @commands.command(name="balance")
    async def balance_voice_members(self, ctx) -> None:
        """
        This command balance your lobby base to members in voice channel, in that you are now.
        If in your voice more or less members that 6, bot answer you what you must do with instruction.
        """
        if ctx.author != self.bot.user:
            if ctx.author.voice is None:
                await reaction(ctx, False)
                await ctx.respond(embed=custom_embed("bvm1"))
            else:
                members_to_balance = {member.name: role.name for member in ctx.author.voice.channel.members
                                      for role in member.roles if role.name in settings["league_roles"]}
                try:
                    async with timeout(settings["time_to_draft_phase_in_seconds"]):
                        clutch = await self.ask_about_players(ctx, members_to_balance)
                except TimeoutError:
                    await ctx.respond(embed=custom_embed("bvm2"))
                await ctx.respond(embed=custom_embed(
                    "bvm3",
                    f"**{', '.join(member for member in clutch[0])}**",
                    f"**{', '.join(member for member in clutch[1])}**")
                )

    async def ask_about_players(self, ctx, members_to_balance: dict[str, str]) -> tuple[list[str], list[str]]:
        """
        This function must refactor code and doing nothing else.

        WARNING: dicts are mutable and this function use it
        """
        while len(members_to_balance) != 6:
            if len(members_to_balance) < 6:
                await ctx.respond(embed=custom_embed("aap1"))
                add_answer = await self.bot.wait_for(
                    "message",
                    check=lambda message: message.author == ctx.author
                )
                members_to_balance += {
                    member.name: role.name for member in add_answer.menttions
                    if member != self.bot.user
                    for role in member.roles
                    if role.name in settings["league_roles"]
                }
                answer_content = [x for x in add_answer.content.split() if "@" not in x]
                for i in range(1, len(answer_content)):
                    members_to_balance[answer_content[i - 1]] = answer_content[i]
            else:
                await ctx.respond(embed=custom_embed("aap2"))
                avoid_answer = await self.bot.wait_for(
                    "message",
                    check=lambda message: message.author == ctx.author
                ).mentions
                members_to_balance = {member_name: members_to_balance[member_name]
                                      for member_name in members_to_balance if member_name not in
                                      [member.name for member in avoid_answer]}

        return balance(convert(members_to_balance))


def setup(bot: BRBot) -> None:
    bot.add_cog(VoiceCog(bot))
