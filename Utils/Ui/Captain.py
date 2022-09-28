from discord import member, Embed, Colour, Message


class Captain:
    draft_chose_message: Message
    draft_state_message: Message

    def __init__(self, ment: member):
        self.ment = ment
        self.bans = []
        self.picks = []

    async def send(self, **kwargs):
        await self.ment.send(**kwargs)

    async def send_and_set_state_message(self) -> None:
        self.draft_state_message = await self.ment.send(embed=self.draft_embed())

    async def send_and_set_chose_message(self, **kwargs) -> None:
        self.draft_chose_message = await self.ment.send(**kwargs)

    @staticmethod
    def draft_embed():
        embed = Embed(title="draft result", colour=Colour.brand_green())
        embed.add_field(name="🟩Your team🟩", value="ban1: _ \npick 1: _ \npick 2: _ \nban2: _ \npick 3: _")
        embed.add_field(name="🟥Opponent's team🟥", value="ban1: _ \npick 1: _ \npick 2: _ \nban2: _ \npick 3: _")
        return embed

    async def update_state_message(self, *characters: str | str) -> None:
        embed = self.draft_state_message.embeds[0]
        for x in 0, 1:
            embed.fields[x].value = embed.fields[x].value.replace("_", characters[x], 1)
        await self.draft_state_message.edit(embed=embed)
