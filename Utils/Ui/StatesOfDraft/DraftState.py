from Utils.Ui.Captain import Captain


class DraftState:
    def __init__(self, draft):
        self.draft = draft

    async def handle(self, character: str, captain: Captain):
        pass
