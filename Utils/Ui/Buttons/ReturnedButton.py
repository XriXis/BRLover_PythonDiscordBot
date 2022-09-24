from discord import Interaction

from Utils.JsonHandler import lst_of_characters
from Utils.MessageLib import custom_embed
from Utils.Ui.Buttons.GroupButton import GroupButton
from Utils.Ui.Buttons.IButton import IButton
from Utils.Ui.Captain import Captain


class ReturnedButton(IButton):
    def __init__(self, capitan: Captain, draft):
        super().__init__("return to last menu", capitan, draft, emoji="↩")

    async def callback(self, interaction: Interaction):
        await interaction.response.edit_message(content=None,
                                                view=self.draft.generate_buttons(lst_of_characters,
                                                                                 GroupButton,
                                                                                 self.captain),
                                                embed=custom_embed(
                                                    self.draft.str_phase == "pick",
                                                    self.draft.str_phase
                                                ))
