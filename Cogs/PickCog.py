from discord.ext import commands
from random import randint

from BRBot import BRBot

from Utils.MessageLib import reaction, custom_embed

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
        self.bot: BRBot = bot

    @commands.command()
    async def team_pick(self, ctx, key: str = None) -> None:
        """
        For ordinary this command give you random team that include 1 melee, 1 range and 1 support,
        but you can change this set using the following keys (args):\n
        `CHAOS` - absolute random team
        """
        # In this function must be smart-sorting of members based on voice context and data-base of person's skills
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
                    await reaction(ctx, False)
                    ctx.respond(embed=custom_embed("tp1", ', '.join(f'`{x}`' for x in lstOfKeys)))
                    return

            await reaction(ctx, True)
            await ctx.respond(embed=custom_embed("tp2", pick))

    @commands.command(name="my_pick")
    async def ones_pick(self, ctx, *group: str) -> None:
        """
        Give you 1 random character. Also, you can specify the group of character, what you want to play. (different
        groups (if you want same) separations with spaces)
        """
        if ctx.author != self.bot.user:
            if len(group) <= 3:
                if not group:
                    group = ['melee', 'range', 'supports']
                if all(x in lstOfCharacters for x in group):
                    sup_lst = [lstOfCharacters[x] for x in group]
                    sup_rand_hero = sup_lst[randint(0, len(sup_lst) - 1)]
                    rand_hero = sup_rand_hero[randint(0, len(sup_rand_hero) - 1)]
                    await reaction(ctx, True)
                    await ctx.respond(embed=custom_embed("op1", rand_hero))
                else:
                    await reaction(ctx, False)
                    await ctx.respond(embed=custom_embed("op2"))
            else:
                await reaction(ctx, False)
                await ctx.respond(embed=custom_embed("op3"))


def setup(bot: BRBot) -> None:
    bot.add_cog(PickCog(bot))
