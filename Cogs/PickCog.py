from discord import Option
from discord.ext import commands
from random import randint

from BRBot import BRBot

from Utils.MessageLib import custom_embed

lstOfCharacters = {
    "melee": ["Bakko", "Croak", "Freya", "Jamila", "Raigon", "Rook", "Ruh Kaan", "Shifu", "Thorn"],
    "range": ['Ashka', 'Alysa', 'Desteny', 'Ezmo', 'Iva', 'Jade', 'Jumong', 'Shen Rao', 'Taya', 'Varesh'],
    "supports": ['Blossom', 'Lucie', 'Oldur', 'Perl', 'Pestilus', 'Poloma', 'Sirius', 'Ulric', 'Zander']
}


class PickCog(commands.Cog):
    """
    This Cog for random-pick commands.
    """

    def __init__(self, bot: BRBot) -> None:
        self.bot = bot

    @commands.slash_command(descroption="Give you random team. Keys: CHAOS")
    async def team_pick(self, ctx, key: Option(str) = None) -> None:
        if ctx.author != self.bot.user:
            lstOfKeys = [
                "CHAOS"
            ]
            match key:
                case None:
                    pick = f"\n||**{lstOfCharacters['melee'][randint(0, 8)]}," + \
                           f"\n{lstOfCharacters['range'][randint(0, 9)]}**|| and..." + \
                           f"\n||***{lstOfCharacters['supports'][randint(0, 8)]}!***||"
                case "CHAOS":
                    pick = "||**"
                    for _ in 0, 0, 0:
                        group = lstOfCharacters[list(lstOfCharacters.keys())[randint(0, 2)]]
                        pick += f"\n{group[randint(0, len(group) - 1)]},"
                    pick += "!**||"
                case _:
                    ctx.respond(embed=custom_embed(False, "tp1", ', '.join(f'`{x}`' for x in lstOfKeys)))
                    return

            await ctx.respond(embed=custom_embed(True, "tp2", pick))

    @commands.slash_command(name="my_pick", description="1 rand hero. Groups separate with spaces")
    async def ones_pick(self, ctx, group: Option(str) = None) -> None:
        if group is None:
            group = ['melee', 'range', 'supports']
        else:
            group = list(group.split())
        if len(group) <= 3:
            if all(x in lstOfCharacters for x in group):
                sup_lst = [lstOfCharacters[x] for x in group]
                sup_rand_hero = sup_lst[randint(0, len(sup_lst) - 1)]
                rand_hero = sup_rand_hero[randint(0, len(sup_rand_hero) - 1)]
                embed = custom_embed(True, "op1", rand_hero)
            else:
                embed = custom_embed(False, "op2")
        else:
            embed = custom_embed(False, "op3")
        await ctx.respond(embed=embed)


def setup(bot: BRBot) -> None:
    bot.add_cog(PickCog(bot))
