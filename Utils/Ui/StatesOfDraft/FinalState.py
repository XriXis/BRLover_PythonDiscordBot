from Utils.MessageLib import custom_embed
from Utils.Ui.Captain import Captain
from Utils.Ui.StatesOfDraft.AbstractDraftState import AbstractDraftState


class FinalState(AbstractDraftState):
    async def handle(self, character: str, captain: Captain):
        captain.picks.append(character)
        if len(self.draft.captain1.picks) == len(self.draft.captain2.picks):
            await self.draft.update_messages(
                self.draft.captain1.picks[-1],
                self.draft.captain2.picks[-1]
            )
            await self.draft.stop()
            await self.draft.global_channel.send(embed=custom_embed(
                True,
                "dr7",
                *self.draft.captain1.picks,
                *self.draft.captain2.picks
            ))
        else:
            captain.timer.chill()

    def to_str(self) -> str:
        return "pick"

    def is_character_occupied(self, character: str, captain: Captain) -> bool:
        return character in captain.bans \
               or character in captain.picks
