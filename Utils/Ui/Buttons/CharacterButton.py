from discord import Interaction

from Utils.MessageLib import custom_embed
from Utils.Ui.Buttons.BaseButton import BaseButton
from Utils.Ui.Captain import Captain
from Utils.Ui.StatesOfDraft.PickState import PickState


class CharacterButton(BaseButton):
    def __init__(self, label, capitan: Captain, draft):
        disabled = draft.is_character_occupied(label, capitan)
        super().__init__(label, capitan, draft, disabled=disabled)

    async def callback(self, interaction: Interaction):
        await interaction.response.edit_message(content=None,
                                                view=None,
                                                embed=custom_embed(
                                                    isinstance(self.draft._state, PickState),
                                                    "empty",
                                                    f"🟩 you ***"
                                                    f"{self.draft._state.to_str()}"
                                                    f"*** {self.label} 🟩"))
        await self.draft.handle(self.label, self.captain)
