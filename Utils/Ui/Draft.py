from asyncio import gather

from discord import member
from discord.ui import View

from Utils.JsonHandler import lst_of_characters
from Utils.MessageLib import custom_embed

from Utils.Ui.Buttons.CharacterButton import CharacterButton
from Utils.Ui.Buttons.GroupButton import GroupButton
from Utils.Ui.Buttons.ReturnedButton import ReturnedButton
from Utils.Ui.Captain import Captain
from Utils.Ui.StatesOfDraft.BanState import BanState
from Utils.Ui.StatesOfDraft.PickState import PickState


class Draft:
    def __init__(self, captain1: member, captain2: member, global_channel):
        self.captain1 = Captain(captain1)
        self.captain2 = Captain(captain2)
        self.phase = 0
        self.order = [BanState(self),
                      PickState(self),
                      PickState(self),
                      BanState(self),
                      PickState(self)]
        self.str_phase = "ban" if self.phase in (0, 3) else "pick"
        self.global_channel = global_channel

    def update_str_phase(self):
        self.str_phase = "ban" if self.order[self.phase] == BanState(self) else "pick"

    def generate_buttons(self,
                         labels: iter,
                         button_cls,
                         capitan: Captain) -> View:
        view_with_buttons = View()
        for label in labels:
            view_with_buttons.add_item(button_cls(label, capitan, self))
        if button_cls == CharacterButton:
            view_with_buttons.add_item(ReturnedButton(capitan, self))
        return view_with_buttons

    async def send_start_of_draft_phase(self):
        await gather(
            self.captain1.send(embed=custom_embed(self.str_phase == "pick", self.str_phase),
                               view=self.generate_buttons(
                                    lst_of_characters,
                                    GroupButton,
                                    self.captain1
                                )),
            self.captain2.send(embed=custom_embed(self.str_phase == "pick", self.str_phase),
                               view=self.generate_buttons(
                                    lst_of_characters,
                                    GroupButton,
                                    self.captain2
                                ))
        )


