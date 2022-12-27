from discord import Interaction

from Utils.JsonHandler import lst_of_characters
from Utils.MessageLib import custom_embed
from SystemsRealisations.DraftSystem.Buttons.BaseButton import BaseButton
from SystemsRealisations.DraftSystem.Buttons.CharacterButton import CharacterButton


class GroupButton(BaseButton):
    async def callback(self, interaction: Interaction):
        await interaction.response.edit_message(content=None,
                                                view=self.draft.generate_buttons(lst_of_characters[self.label],
                                                                                 CharacterButton,
                                                                                 self.captain),
                                                embed=custom_embed(
                                                    str(self.draft._state) == "pick",
                                                    "empty",
                                                    f"✅ you choose to **"
                                                    f"{str(self.draft._state)}**"
                                                    f" {self.label} characters ✅"
                                                ))
