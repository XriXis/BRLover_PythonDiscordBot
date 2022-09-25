from asyncio import gather

from discord import member
from discord.ui import View

from Utils.JsonHandler import lst_of_characters, settings
from Utils.MessageLib import custom_embed

from Utils.Ui.Buttons.CharacterButton import CharacterButton
from Utils.Ui.Buttons.GroupButton import GroupButton
from Utils.Ui.Buttons.ReturnedButton import ReturnedButton
from Utils.Ui.Captain import Captain
from Utils.Ui.StatesOfDraft.AbstractDraftState import AbstractDraftState
from Utils.Ui.StatesOfDraft.BanState import BanState
from Utils.Ui.StatesOfDraft.PickState import PickState


class Draft:
    _state: AbstractDraftState

    def __init__(self, captain1: member, captain2: member, global_channel):
        self.captain1 = Captain(captain1)
        self.captain2 = Captain(captain2)
        self.order = iter(["ban", "pick", "pick", "ban", "pick"])
        self.global_channel = global_channel
        self.update_state()

    def update_state(self):
        self._state = BanState(self) if next(self.order) == "ban" else PickState(self)

    def is_character_occupied(self, character: str, captain: Captain) -> bool:
        return self._state.is_character_occupied(character, captain)

    async def handle(self, character: str, capitan: Captain):
        await self._state.handle(character, capitan)

    def generate_buttons(self,
                         labels: iter,
                         button_cls,
                         capitan: Captain) -> View:
        view_with_buttons = View(timeout=settings["time_to_draft_phase_in_seconds"])
        for label in labels:
            view_with_buttons.add_item(button_cls(label, capitan, self))
        if button_cls == CharacterButton:
            view_with_buttons.add_item(ReturnedButton(capitan, self))
        return view_with_buttons

    async def send_start_of_draft_phase(self):
        await gather(
            self.captain1.send(embed=custom_embed(isinstance(self._state, PickState), self._state.__class__.__name__),
                               view=self.generate_buttons(
                                   lst_of_characters,
                                   GroupButton,
                                   self.captain1
                               )),
            self.captain2.send(embed=custom_embed(isinstance(self._state, PickState), self._state.__class__.__name__),
                               view=self.generate_buttons(
                                   lst_of_characters,
                                   GroupButton,
                                   self.captain2
                               ))
        )
