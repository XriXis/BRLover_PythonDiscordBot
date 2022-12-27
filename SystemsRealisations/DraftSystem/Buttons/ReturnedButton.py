from discord import Interaction

from Utils.JsonHandler import lst_of_characters
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
                                                    str(self.draft._state) == "pick",
                                                    str(self.draft._state)
                                                ))
