from discord import Option
from discord.ext import commands

from BRBot import BRBot
from Utils.MessageLib import custom_embed
from Utils.JsonHandler import change_prefix_in_data, settings, change_lang_in_data


class AdminCog(commands.Cog):
    """
    This cog for administrate the bot or administrate the guild using bots hands.
    """

    def __init__(self, bot: BRBot) -> None:
        self.bot: BRBot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence_to_help()

    @commands.slash_command(description="for prefix-command")
    @commands.has_role(settings["privileged role"])
    async def change_prefix(self, ctx, new_prefix: Option(str)) -> None:

        if str_without_spaces(new_prefix) == "":
            embed = custom_embed(False, "chp1")
        elif new_prefix == "/":
            embed = custom_embed(False, "chp2")
        elif " " in new_prefix:
            embed = custom_embed(False, "chp3")
        else:
            embed = custom_embed(True, "chp4")
            change_prefix_in_data(new_prefix)
            self.bot.command_prefix = new_prefix
            await self.bot.change_presence_to_help()
        await ctx.respond(embed=embed)

    @commands.slash_command(description="must reboot bot")
    @commands.has_role(settings["privileged role"])
    async def change_language(self, ctx, lang: Option(str, choices=["RU", "ENG"])):
        change_lang_in_data(lang)
        await ctx.respond(embed=custom_embed(True, "chl2"))


def str_without_spaces(text: str) -> str:
    result = ""
    for char in text:
        if char != "":
            result += char
    return result


def setup(bot: BRBot) -> None:
    bot.add_cog(AdminCog(bot))
