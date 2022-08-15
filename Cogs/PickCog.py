from discord.ext import commands
from random import randint

from BRBot import BRBot

from Utils.MessageLib import reaction

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
                    ctx.reply("Unknown  keyword, please use only next one of the conditions: " +
                              f"*{', '.join(f'`{x}`' for x in lstOfKeys)}*" +
                              "\n\n**Or don't give any key and your pick will ordinary**")
                    return

            await reaction(ctx, True)
            await ctx.reply(f"And your dream-team is...{pick}")

    @commands.command()
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
                    sup_randHero = sup_lst[randint(0, len(sup_lst) - 1)]
                    randHero = sup_randHero[randint(0, len(sup_randHero) - 1)]
                    await reaction(ctx, True)
                    await ctx.reply(f"And your pick is... ||**{randHero}!**||")
                else:
                    await reaction(ctx, False)
                    await ctx.reply("Battlerite have 3 group of characters: meele, range and supports." +
                                    "Please, use THIS keywords to use this function.")
            else:
                await reaction(ctx, False)
                await ctx.reply("Battlerite have only 3 group of characters, and you given more.")


def setup(bot: BRBot) -> None:
    bot.add_cog(PickCog(bot))
