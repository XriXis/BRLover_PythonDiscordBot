from Utils.MessageLib import custom_embed
from Utils.Ui.Captain import Captain
from Utils.Ui.StatesOfDraft.DraftState import DraftState


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
            await self.draft.captain2.send(embed=custom_embed(True, "dr5", self.draft.captain2.bans[-1]))
            await self.draft.captain1.send(embed=custom_embed(True, "dr5", self.draft.captain1.bans[-1]))
            await self.draft.send_start_of_draft_phase()
