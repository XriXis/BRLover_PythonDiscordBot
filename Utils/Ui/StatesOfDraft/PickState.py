from Utils.Ui.Captain import Captain
from Utils.Ui.StatesOfDraft.AbstractDraftState import AbstractDraftState


class PickState(AbstractDraftState):
    async def handle(self, character: str, captain: Captain):
        captain.picks.append(character)
        if len(self.draft.captain1.picks) == len(self.draft.captain2.picks):
            self.draft.update_state()
            await self.draft.update_messages(
                self.draft.captain1.picks[-1],
                self.draft.captain2.picks[-1]
            )
            captain.timer.reset()
        else:
            captain.timer.chill()

    def to_str(self) -> str:
        return "pick"

    def is_character_occupied(self, character: str, captain: Captain) -> bool:
        return character in captain.bans \
               or character in captain.picks
