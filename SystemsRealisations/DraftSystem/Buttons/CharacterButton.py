from discord import Interaction

from Utils.MessageLib import custom_embed
from SystemsRealisations.DraftSystem.Buttons.BaseButton import BaseButton
from SystemsRealisations.DraftSystem.Captain import Captain


class CharacterButton(BaseButton):
    def __init__(self, label, capitan: Captain, draft):
        disabled = draft.is_character_occupied(label, capitan)
        super().__init__(label, capitan, draft, disabled=disabled)

    async def callback(self, interaction: Interaction):
        await interaction.response.edit_message(content=None,
                                                view=None,
                                                embed=custom_embed(
                                                    str(self.draft._state) == "pick",
                                                    "empty",
                                                    f"🟩 you ***"
                                                    f"{str(self.draft._state)}"
                                                    f"*** {self.label} 🟩"))
        await self.draft.handle(self.label, self.captain)
