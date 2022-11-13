from discord import SelectOption, Interaction
from discord.ui import Select, View, Modal, InputText

from Utils.JsonHandler import settings
from Utils.MessageLib import custom_embed


# Errors: cycle of choices, can't select uniq league, can't use little number of character in modal
class StrangersSelectMenu(Select):
    def __init__(self, clutch):
        self.clutch = clutch
        super().__init__(
            placeholder="Choose play lvl of unknown player",
            min_values=1,
            max_values=1,
            options=[
                SelectOption(label=role, value=role)
                for role in settings["league_roles"]
            ]
        )

    async def callback(self, interaction: Interaction) -> None:
        name_input = InputText(label='input name. ***MUST BE UNIQ***',
                               placeholder="XriXis, for example",
                               min_length=0,
                               max_length=25)
        modal = Modal(name_input, title="Stranger name. (>3 char)")

        async def modal_callback(m_interaction: Interaction) -> None:
            self.clutch.strangers[
                name_input.value
                if len(name_input.value) > 3 else
                self._stranger_name()
            ] = (self.values[0])

            if len(self.clutch.strangers) + len(self.clutch.members) != 6:
                view = View()
                self.placeholder = "Choose play lvl of unknown player, again"
                view.add_item(self)
                await m_interaction.response.edit_message(
                    embed=custom_embed(
                        True,
                        "chose again",
                        ", ".join(list(member.name for member in self.clutch.members) +
                                  list(self.clutch.strangers.keys()))),
                    view=view
                )
            else:
                await m_interaction.response.edit_message(content="all good", delete_after=1)
                await self.clutch.start_balance()
            self.values.clear()

        modal.callback = modal_callback
        await interaction.response.send_modal(modal)

    def _stranger_name(self, _index=1) -> str:
        name = f"{self.values[0]} player {_index}"
        if name not in self.clutch.strangers:
            return name
        else:
            return self._stranger_name(_index + 1)
