from abc import ABC, abstractmethod

from SystemsRealisations.DraftSystem.Captain import Captain


class AbstractDraftState(ABC):
    def __init__(self, draft):
        self.draft = draft
        super().__init__()

    @abstractmethod
    async def handle(self, character: str, captain: Captain):
        pass

    @abstractmethod
    def is_character_occupied(self, character: str, captain: Captain):
        pass
