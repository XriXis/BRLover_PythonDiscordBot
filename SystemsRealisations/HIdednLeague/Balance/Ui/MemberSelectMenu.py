from discord import SelectOption, Interaction
from discord.ui import Select

from Utils.MessageLib import custom_embed


class MembersSelectMenu(Select):
    def __init__(self, clutch):
        self.clutch = clutch
        super().__init__(
            placeholder="Choose who afk",
            min_values=len(clutch.members) - 6 if len(clutch.members) > 6 else 1,
            max_values=len(clutch.members),
            options=[
                        SelectOption(label=member.name, value=member.name)
                        for member in clutch.members
                    ] + ([SelectOption(label="no one", value="no one")] if len(clutch.members) <= 6 else [])
        )

    async def callback(self, interaction: Interaction):
        if len(self.clutch.members) - len(self.values) > 6 and "no one" not in self.values:
            await interaction.response.edit_message(embed=custom_embed(False, "so much players in voice"),
                                                    delete_after=15)
        else:
            if "no one" not in self.values:
                for name in self.values:
                    self.clutch.exclude(name)
            await interaction.response.edit_message(content="Ok", delete_after=1)
            if len(self.clutch.members) < 6:
                await self.clutch.who_else()
                await interaction.message.delete()
            else:
                await self.clutch.start_balance()
                await interaction.message.delete()
