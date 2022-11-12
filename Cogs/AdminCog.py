from discord import Option, SelectOption, Interaction
from discord.ext import commands
from discord.ui import View, Select

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

    @commands.Cog.listener()
    async def on_member_join(self, member):
        view = View()
        menu = Select(
            placeholder="choose",
            min_values=1,
            max_values=len(settings["game_roles"]),
            options=[
                SelectOption(label=game, value=game, description=settings["game_roles"][game])
                for game in settings["game_roles"]])

        async def callback(interaction: Interaction):
            await member.add_roles(
                role.id for role in member.guild.roles if (role.name in menu.values and role.name != "Battlerite"))
            if "Battlerite" not in menu.values:
                await interaction.response.edit_message(content="tnx", embed=None, view=None, delete_after=10)
            else:
                role_view = View()
                role_menu = Select(
                    placeholder="choose your play lvl in BR",
                    min_values=1,
                    max_values=1,
                    options=[
                        SelectOption(label=league, value=league)
                        for league in settings["league_roles"]])

                async def role_callback(role_interaction: Interaction):
                    await member.add_roles(
                        role.id for role in member.guild.roles if role.name == role_menu.values[0])
                    await interaction.response.edit_message(content="tnx", embed=None, view=None, delete_after=10)

                role_menu.callback = role_callback
                await interaction.response.edit_message(embed=custom_embed(True, "new BR member"), view=role_view)

        menu.callback = callback
        view.add_item(menu)
        await member.send(
            embed=custom_embed(True, "new_member"),
            view=view
        )

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
