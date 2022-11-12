from discord import Interaction

from Utols.JsonHandler import lst_of_characters
from Utils.MessageLib import custom_embed
from SystemsRealisations.DraftSystem.Buttons.BaseButton import BaseButton
from SystemsRealisations.DraftSystem.Buttons.GroupButton import GroupButton
from SystemsRealisations.DraftSystem.Captain import Captain


class ReturnedButton(BaseButton):
    def __init__(self, capitan: Captain, draft):
        super().__init__("return to last menu", capitan, draft, emoji="↩")

    async def callback(self, interaction: Interaction):
        await interaction.response.edit_message(content=None,
                                                view=self.draft.generate_buttons(lst_of_characters,
                                                                                 GroupButton,
                                                                                 self.captain),
                                                embed=custom_embed(
                                                    self.draft._state.to_str() == "pick",
                                                    self.draft._state.to_str()
                                                ))
