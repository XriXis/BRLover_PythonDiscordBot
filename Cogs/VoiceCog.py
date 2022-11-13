from discord.ext import commands
from BRBot import BRBot
from SystemsRealisations.HIdednLeague.Balance.Clutch import Clutch
from Utils.MessageLib import custom_embed
from Utils.JsonHandler import settings


class VoiceCog(commands.Cog):
    """
    This cog includes commands that must have permission to work with voice channels
    """

    def __init__(self, bot: BRBot) -> None:
        self.bot: BRBot = bot

    @commands.slash_command(description="Can use only moders. Change your voice to bigger")
    @commands.has_role(settings["privileged role"])
    async def move_us(self, ctx):
        if ctx.author.voice is None:
            embed = custom_embed(False, "mu1")
        else:
            ok = False
            for channelTo in ctx.guild.voice_channels:
                if (ctx.author.voice.channel.user_limit < channelTo.user_limit or channelTo.user_limit == 0) \
                        and (len(channelTo.members) < 2):
                    ok = True
                    break
            if not ok:
                embed = custom_embed(False, "mu2")
            elif channelTo == ctx.author.voice.channel:
                embed = custom_embed(False, "mu3")
            else:
                for member in ctx.author.voice.channel.members:
                    await member.move_to(channelTo)
                embed = custom_embed(True, "mu4")
        await ctx.respond(embed=embed)

    @commands.slash_command(name="balance", description="balance voice member like them in BR lobby")
    async def balance_voice_members(self, ctx) -> None:
        if ctx.author.voice is not None:
            await ctx.respond("ok", delete_after=1)
            clutch = Clutch(ctx.author.voice.channel.members, ctx.channel, {})
            await clutch.who_afk()
        else:
            await ctx.respond(embed=custom_embed(False, "mu1"))


def setup(bot: BRBot) -> None:
    bot.add_cog(VoiceCog(bot))
