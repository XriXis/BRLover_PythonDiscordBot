from Utils.MessageLib import custom_embed
from Utils.Ui.Captain import Captain
from Utils.Ui.StatesOfDraft.AbstractDraftState import AbstractDraftState


class BanState(AbstractDraftState):
    async def handle(self, character: str, captain: Captain) -> None:
        if captain is self.draft.captain1:
            self.draft.captain2.bans.append(character)
        else:
            self.draft.captain1.bans.append(character)
        if len(self.draft.captain1.bans) == len(self.draft.captain2.bans):
            self.draft.update_state()
            await self.draft.update_messages(
                self.draft.captain2.bans[-1],
                self.draft.captain1.bans[-1]
            )

    def to_str(self) -> str:
        return "ban"

    def is_character_occupied(self, character: str, captain: Captain) -> bool:
        if captain is self.draft.captain1:
            return character in self.draft.captain2.picks \
                   or character in self.draft.captain2.bans
        else:
            return character in self.draft.captain1.picks \
                   or character in self.draft.captain1.bans
