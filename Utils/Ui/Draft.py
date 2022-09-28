from asyncio import sleep

from discord import member, Embed
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

    def generate_draft_choose_messages(self) -> tuple[dict[str, View | Embed], ...]:
        return tuple(
            {'embed': custom_embed(
                isinstance(self._state, PickState),
                self._state.__class__.__name__),
             'view': self.generate_buttons(
                lst_of_characters,
                GroupButton,
                captain)
            } for captain in (self.captain1, self.captain2))

    async def update_captains_choose_messages(self) -> None:
        args = self.generate_draft_choose_messages()
        await self.captain1.draft_chose_message.edit(**args[0])
        await self.captain2.draft_chose_message.edit(**args[1])

    async def update_captains_state_messages(self, chose_1st_captain: str, chose_2nd_captain: str) -> None:
        await self.captain1.update_state_message(chose_1st_captain, chose_2nd_captain)
        await self.captain2.update_state_message(chose_2nd_captain, chose_1st_captain)

    async def send_state_messages(self) -> None:
        await self.captain1.send_and_set_state_message()
        await self.captain2.send_and_set_state_message()

    async def send_chose_messages(self) -> None:
        args = self.generate_draft_choose_messages()
        await self.captain1.send_and_set_chose_message(**args[0])
        await self.captain2.send_and_set_chose_message(**args[0])
