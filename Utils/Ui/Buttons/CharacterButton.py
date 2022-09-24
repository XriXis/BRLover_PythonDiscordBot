from discord import Interaction

from Utils.MessageLib import custom_embed
from Utils.Ui.Buttons.IButton import IButton
from Utils.Ui.Captain import Captain


class CharacterButton(IButton):
    def __init__(self, label, capitan: Captain, draft):
        super().__init__(label, capitan, draft, disabled=(label in capitan.picks) or (label in capitan.bans))
        self.State = self.draft.order[draft.phase]
        self.str_phase_draft = self.draft.str_phase

    async def callback(self, interaction: Interaction):
        await interaction.response.edit_message(content=None,
                                                view=None,
                                                embed=custom_embed(self.str_phase_draft == "pick",
                                                                   "empty",
                                                                   f"🟩 you ***{self.str_phase_draft}*** {self.label} 🟩"))
        await self.State.handle(self.label, self.captain)
