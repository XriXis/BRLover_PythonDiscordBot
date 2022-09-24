from discord import Option
from discord.ext import commands
from random import randint

from BRBot import BRBot
from Utils.JsonHandler import lst_of_characters

from Utils.MessageLib import custom_embed


class PickCog(commands.Cog):
    """
    This Cog for random-pick commands.
    """

    def __init__(self, bot: BRBot) -> None:
        self.bot = bot

    @commands.slash_command(name="team_pick", description="Give you random team. Keys: standard, CHAOS")
    async def team_pick(self, ctx, key: Option(str) = None) -> None:
        # TODO: chose of exclude
        if ctx.author != self.bot.user:
            lst_of_keys = [
                "CHAOS"
            ]
            match key:
                case None:
                    pick = f"\n||**{lst_of_characters['melee'][randint(0, 8)]}," + \
                           f"\n{lst_of_characters['range'][randint(0, 9)]}**|| and..." + \
                           f"\n||***{lst_of_characters['supports'][randint(0, 8)]}!***||"
                case "CHAOS":
                    pick = "||**"
                    for _ in 0, 0, 0:
                        group = lst_of_characters[list(lst_of_characters.keys())[randint(0, 2)]]
                        pick += f"\n{group[randint(0, len(group) - 1)]},"
                    pick += "!**||"
                case _:
                    await ctx.respond(embed=custom_embed(False, "tp1", ', '.join(f'`{x}`' for x in lst_of_keys)))
                    return

            await ctx.respond(embed=custom_embed(True, "tp2", pick))

    @commands.slash_command(name="my_pick", description="1 rand hero. Groups separate with spaces")
    async def ones_pick(self, ctx, group: Option(str) = None) -> None:
        if group is None:
            group = ['melee', 'range', 'supports']
        else:
            group = list(group.split())
        if len(group) <= 3:
            if all(x in lst_of_characters for x in group):
                sup_lst = [lst_of_characters[x] for x in group]
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
