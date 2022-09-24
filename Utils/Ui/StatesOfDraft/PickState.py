from Utils.MessageLib import custom_embed
from Utils.Ui.Captain import Captain
from Utils.Ui.StatesOfDraft.DraftState import DraftState


class PickState(DraftState):
    async def handle(self, character: str, captain: Captain):
        captain.picks.append(character)
        if len(self.draft.captain1.picks) == len(self.draft.captain2.picks):
            if self.draft.phase == 5:
                await self.draft.global_channel.send(embed=custom_embed(True, "dr7"))
            else:
                self.draft.phase += 1
                self.draft.update_str_phase()
                await self.draft.captain2.send(embed=custom_embed(False, "dr5", self.draft.captain1.picks[-1]))
                await self.draft.captain1.send(embed=custom_embed(False, "dr5", self.draft.captain2.picks[-1]))
                await self.draft.send_start_of_draft_phase(self.draft)
