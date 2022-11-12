from discord import SelectOption, Interaction
from discord.ui import Select, View

from Utols.JsonHandler import settings
from Utils.MessageLib import custom_embed


class StrangersSelectMenu(Select):
    def __init__(self, clutch):
        self.clutch = clutch
        super().__init__(
            placeholder="Choose play lvl of unknown player",
            min_values=1,
            max_values=1,
            options=[
                SelectOption(label=role, value=role)
                for role in settings["league_roles"]
            ]
        )

    async def callback(self, interaction: Interaction):
        self.clutch.strangers.append(self.values[0])
        if len(self.clutch.strangers) + len(self.clutch.members) != 6:
            view = View()
            self.placeholder = "Choose play lvl of unknown player, again"
            view.add_item(self)
            await interaction.response.edit_message(
                embed=custom_embed(True, "chose again"),
                view=view
            )
        else:
            await self.clutch.start_balance()
            await interaction.message.delete()
