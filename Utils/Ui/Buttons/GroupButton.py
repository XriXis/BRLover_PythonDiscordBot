from discord import Interaction

from Utils.JsonHandler import lst_of_characters
from Utils.MessageLib import custom_embed
from Utils.Ui.Buttons.CharacterButton import CharacterButton
from Utils.Ui.Buttons.IButton import IButton


class GroupButton(IButton):
    async def callback(self, interaction: Interaction):
        await interaction.response.edit_message(content=None,
                                                view=self.draft.generate_buttons(lst_of_characters[self.label],
                                                                                 CharacterButton,
                                                                                 self.captain),
                                                embed=custom_embed(
                                                    self.draft.str_phase == "pick",
                                                    "empty",
                                                    f"✅ you choose to **{self.draft.str_phase}** {self.label} characters ✅"
                                                ))
