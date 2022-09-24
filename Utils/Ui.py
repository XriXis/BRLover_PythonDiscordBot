from asyncio import gather

from discord.ui import Button, View
from discord import ButtonStyle, Interaction, member

from Utils.JsonHandler import lst_of_characters
from Utils.MessageLib import custom_embed


class Draft:
    def __init__(self, captain1: member, captain2: member, global_channel):
        self.captain1 = Captain(captain1)
        self.captain2 = Captain(captain2)
        self.phase = 0
        self.order = [BanState(self), PickState(self), PickState(self), BanState(self), PickState(self)]
        self.str_phase = "ban" if self.order[self.phase] == BanState(self) else "pick"
        self.global_channel = global_channel

    def update_str_phase(self):
        self.str_phase = "ban" if self.order[self.phase] == BanState(self) else "pick"


class Captain:
    def __init__(self, ment: member):
        self.ment = ment
        self.bans = []
        self.picks = []

    async def send(self, **kwargs):
        await self.ment.send(**kwargs)


class GroupButton(Button):
    def __init__(self, label: str, capitan: Captain, draft: Draft):
        colour = get_colour_by_button(label)
        super().__init__(style=colour, label=label)
        self.captain = capitan
        self.draft = draft

    async def callback(self, interaction: Interaction):
        await interaction.response.edit_message(content=None,
                                                view=generate_buttons(lst_of_characters[self.label],
                                                                      CharacterButton,
                                                                      self.captain,
                                                                      self.draft),
                                                embed=custom_embed(
                                                    self.draft.str_phase == "pick",
                                                    "empty",
                                                    f"✅ you choose to **{self.draft.str_phase}** {self.label} characters ✅"
                                                ))


class CharacterButton(Button):
    def __init__(self, label, capitan: Captain, draft: Draft):
        colour = get_colour_by_button(label)
        super().__init__(style=colour, label=label, disabled=(label in capitan.picks) or (label in capitan.bans))
        self.captain = capitan
        self.State = draft.order[draft.phase]
        self.str_phase_draft = draft.str_phase

    async def callback(self, interaction: Interaction):
        await interaction.response.edit_message(content=None,
                                                view=None,
                                                embed=custom_embed(self.str_phase_draft == "pick",
                                                                   "empty",
                                                                   f"✅ you ***{self.str_phase_draft}*** {self.label} ✅"))
        await self.State.handle(self.label, self.captain)


class ReturnedButton(Button):
    def __init__(self, capitan: Captain, draft: Draft):
        super().__init__(style=ButtonStyle.gray,
                         label="return to last menu",
                         emoji="↩")
        self.captain = capitan
        self.draft = draft

    async def callback(self, interaction: Interaction):
        await interaction.response.edit_message(content=None,
                                                view=generate_buttons(lst_of_characters,
                                                                      GroupButton,
                                                                      self.captain,
                                                                      self.draft),
                                                embed=custom_embed(
                                                    self.draft.str_phase == "pick",
                                                    self.draft.str_phase
                                                ))


class DraftState:
    def __init__(self, draft: Draft):
        self.draft = draft

    async def handle(self, character: str, captain: Captain):
        pass


class BanState(DraftState):
    async def handle(self, character: str, captain: Captain):
        if captain is self.draft.captain1:
            await self._support(character, self.draft.captain2)
        else:
            await self._support(character, self.draft.captain1)

    async def _support(self, character: str, captain: Captain):
        captain.bans.append(character)
        if len(self.draft.captain1.bans) == len(self.draft.captain2.bans):
            self.draft.phase += 1
            self.draft.update_str_phase()
            await send_start_of_draft_phase(self.draft)


class PickState(DraftState):
    async def handle(self, character: str, captain: Captain):
        captain.picks.append(character)
        if len(self.draft.captain1.picks) == len(self.draft.captain2.picks):
            if self.draft.phase == 5:
                await self.draft.global_channel.send(embed=custom_embed(True, "dr7"))
            else:
                self.draft.phase += 1
                self.draft.update_str_phase()
                await send_start_of_draft_phase(self.draft)


def get_colour_by_button(label: str):
    if label in lst_of_characters:
        group = label
    else:
        group = [[x for x in lst_of_characters if label in lst_of_characters[x]] + [None]][0][0]

    if group == "melee":
        colour = ButtonStyle.red
    elif group == "range":
        colour = ButtonStyle.primary  # blue
    elif group == "supports":
        colour = ButtonStyle.success  # green
    else:
        colour = ButtonStyle.gray
    return colour


def generate_buttons(labels: iter,
                     button_cls,
                     capitan: Captain,
                     draft: Draft) -> View:
    view_with_buttons = View()
    for label in labels:
        view_with_buttons.add_item(button_cls(label, capitan, draft))
    if button_cls == CharacterButton:
        view_with_buttons.add_item(ReturnedButton(capitan, draft))
    return view_with_buttons


async def send_start_of_draft_phase(draft):
    await gather(
        draft.captain1.send(embed=custom_embed(draft.str_phase == "pick", draft.str_phase),
                            view=generate_buttons(
                                lst_of_characters,
                                GroupButton,
                                draft.captain1,
                                draft
                            )),
        draft.captain2.send(embed=custom_embed(draft.str_phase == "pick", draft.str_phase),
                            view=generate_buttons(
                                lst_of_characters,
                                GroupButton,
                                draft.captain2,
                                draft
                            ))
    )
