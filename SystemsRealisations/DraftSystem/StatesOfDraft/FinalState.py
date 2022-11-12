from Utils.MessageLib import custom_embed
from SystemsRealisations.DraftSystem.Captain import Captain
from SystemsRealisations.DraftSystem.StatesOfDraft.AbstractDraftState import AbstractDraftState


class FinalState(AbstractDraftState):
    async def handle(self, character: str, captain: Captain):
        captain.picks.append(character)
        if len(self.draft.captain1.picks) == len(self.draft.captain2.picks):
            await self.draft.update_messages(
                self.draft.captain1.picks[-1],
                self.draft.captain2.picks[-1],
                is_final=True
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
