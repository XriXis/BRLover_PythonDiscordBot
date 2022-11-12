from discord import Interaction

from Utols.JsonHandler import lst_of_characters
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
                                                    self.draft._state.to_str() == "pick",
                                                    "empty",
                                                    f"✅ you choose to **"
                                                    f"{self.draft._state.to_str()}**"
                                                    f" {self.label} characters ✅"
                                                ))
