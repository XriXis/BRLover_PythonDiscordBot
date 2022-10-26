from asyncio import gather, TimeoutError as ATimeoutError

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
from Utils.Ui.StatesOfDraft.FinalState import FinalState
from Utils.Ui.StatesOfDraft.PickState import PickState


class Draft:
    _state: AbstractDraftState

    def __init__(self, captain1: member, captain2: member, global_channel):
        self.captain1 = Captain(captain1)
        self.captain2 = Captain(captain2)
        self.order = iter(["ban", "pick", "pick", "ban", "final_pick"])
        self.global_channel = global_channel
        self.update_state()

    def update_state(self):
        next_state = next(self.order)
        self._state = \
            BanState(self) if next_state == "ban" \
            else PickState(self) if next_state == "pick" \
            else FinalState(self)

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

    async def start(self):
        try:
            await gather(
                self.captain1.start(embed=custom_embed(self._state.to_str() == "pick", self._state.to_str()),
                                    view=self.generate_buttons(
                                        lst_of_characters,
                                        GroupButton,
                                        self.captain1
                                    )),
                self.captain2.start(embed=custom_embed(self._state.to_str() == "pick", self._state.to_str()),
                                    view=self.generate_buttons(
                                        lst_of_characters,
                                        GroupButton,
                                        self.captain2
                                    ))
            )
        except ATimeoutError:
            await self.stop()
            await self.global_channel.send(embed=custom_embed(False, "dr6"))

    async def stop(self):
        await self.captain1.stop()
        await self.captain2.stop()

    async def update_messages(self, chose_1st_cap, chose_2nd_cap):
        await gather(
            self.captain1.update_messages(chose_1st_cap,
                                          chose_2nd_cap,
                                          state=self._state.to_str(),
                                          view=self.generate_buttons(
                                              lst_of_characters,
                                              GroupButton,
                                              self.captain1),
                                          is_final=isinstance(self._state, FinalState)),
            self.captain2.update_messages(chose_2nd_cap,
                                          chose_1st_cap,
                                          state=self._state.to_str(),
                                          view=self.generate_buttons(
                                              lst_of_characters,
                                              GroupButton,
                                              self.captain2),
                                          is_final=isinstance(self._state, FinalState))
        )
