from discord import Option
from discord.ext import commands

from BRBot import BRBot
from Utols.JsonHandler import settings
from Utils.MessageLib import custom_embed


class StateCog(commands.Cog):
    def __init__(self, bot: BRBot) -> None:
        self.bot: BRBot = bot

    @commands.slash_command(description='Give the state of character without "lobby-effect"')
    async def my_true_state(
            self,
            ctx,
            games: Option(int),
            win_rate: Option(float),
            lvl: Option(int),
            current_exp: Option(int)):
        if any(x is None for x in (games, win_rate, lvl, current_exp)):
            await ctx.respond(embed=custom_embed(False, "mts1", *[settings["prefix"]] * 2))
        else:
            lvlExp = [255, 316, 393, 486, 604, 754, 938, 1165, 1443,
                      2500, 3000, 3500, 4000, 5000, 6000, 7000, 8000,
                      8000, 8000, 18000, 26000, 36000, 46000, 56000,
                      66000, 76000, 86000, 96000, 106000, 116000]
            win_rate /= 100
            allExp = current_exp + sum(lvlExp[:lvl - 1])
            loose = (1 - win_rate) * games
            winExp = allExp - loose * 100
            wins = winExp / 200
            trueGames = wins + loose
            trueWinRates = (wins / trueGames) * 1000 // 1 / 10
            await ctx.respond(True, "mts2", str(trueGames // 1), str(trueWinRates))


def setup(bot: BRBot) -> None:
    bot.add_cog(StateCog(bot))
