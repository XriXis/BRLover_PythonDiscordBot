from SystemsRealisations.DraftSystem.StatesOfDraft.PickState import PickState
from Utils.MessageLib import custom_embed
from SystemsRealisations.DraftSystem.Captain import Captain


class FinalState(PickState):
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
