from Utils.MessageLib import custom_embed
from Utils.Ui.Captain import Captain
from Utils.Ui.StatesOfDraft.AbstractDraftState import AbstractDraftState


class PickState(AbstractDraftState):
    async def handle(self, character: str, captain: Captain):
        captain.picks.append(character)
        if len(self.draft.captain1.picks) == len(self.draft.captain2.picks):
            if 3 == len(self.draft.captain1.picks):
                await self.draft.global_channel.send(embed=custom_embed(
                    True,
                    "dr7",
                    *self.draft.captain1.picks,
                    *self.draft.captain2.picks
                ))
            else:
                self.draft.update_state()
                await self.draft.captain2.send(embed=custom_embed(True, "dr5", self.draft.captain1.picks[-1]))
                await self.draft.captain1.send(embed=custom_embed(True, "dr5", self.draft.captain2.picks[-1]))
                await self.draft.send_start_of_draft_phase()

    def to_str(self) -> str:
        return "pick"

    def is_character_occupied(self, character: str, captain: Captain) -> bool:
        return character in captain.bans \
               or character in captain.picks
