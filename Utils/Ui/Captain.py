from discord import member


class Captain:
    def __init__(self, ment: member):
        self.ment = ment
        self.bans = []
        self.picks = []

    async def send(self, **kwargs):
        await self.ment.send(**kwargs)
