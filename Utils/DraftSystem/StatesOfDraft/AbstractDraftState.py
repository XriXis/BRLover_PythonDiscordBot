from Utils.DraftSystem.Captain import Captain


class AbstractDraftState:
    def __init__(self, draft):
        self.draft = draft

    async def handle(self, character: str, captain: Captain):
        pass

    def to_str(self):
        pass

    def is_character_occupied(self, character: str, captain: Captain):
        pass
