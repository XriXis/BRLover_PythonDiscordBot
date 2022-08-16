from discord.ext import commands, bridge

from BRBot import BRBot
from Utils.JsonHandler import settings
from Utils.MessageLib import reaction, custom_embed


class StateCog(commands.Cog):
    def __init__(self, bot: BRBot) -> None:
        self.bot: BRBot = bot

    # TO DO: add text input and take from this slash-command
    @commands.command()
    async def my_true_state(
            self,
            ctx,
            games: int = None,
            winRate: float = None,
            lvl: int = None,
            currentExp: int = None,
            *args):
        """
         TO DO: this documentation
        """
        if ctx.author != self.bot.user:
            if any(x is None for x in (games, winRate, lvl, currentExp)):
                await reaction(ctx, False)
                await ctx.respond(embed=custom_embed("mts1", *[settings["prefix"]] * 2))
            else:
                await reaction(ctx, True)
                lvlExp = [255, 316, 393, 486, 604, 754, 938, 1165, 1443,
                          2500, 3000, 3500, 4000, 5000, 6000, 7000, 8000,
                          8000, 8000, 18000, 26000, 36000, 46000, 56000,
                          66000, 76000, 86000, 96000, 106000, 116000]
                winRate /= 100
                allExp = currentExp + sum(lvlExp[:lvl - 1])
                loose = (1 - winRate) * games
                winExp = allExp - loose * 100
                wins = winExp / 200
                trueGames = wins + loose
                trueWinRates = (wins / trueGames) * 1000 // 1 / 10
                await ctx.respond("mts2", str(trueGames // 1), str(trueWinRates))


def setup(bot: BRBot) -> None:
    bot.add_cog(StateCog(bot))
