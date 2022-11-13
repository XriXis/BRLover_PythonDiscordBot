from discord import member, Embed, Colour, Message
from discord.ui import View

from Utils.JsonHandler import settings
from Utils.MessageLib import custom_embed
from SystemsRealisations.DraftSystem.TimerMessage import TimerMessage


class Captain:
    _draft_message: Message
    _chose_message: Message
    timer: TimerMessage

    def __init__(self, ment: member):
        self.ment = ment
        self.bans = []
        self.picks = []

    async def start(self, **kwargs_of_chose_message):
        self._draft_message = await self._send_draft_message()
        self._chose_message = await self.ment.send(**kwargs_of_chose_message)
        self.timer = TimerMessage(settings["time_to_draft_phase_in_seconds"])
        await self.timer.send(self.ment)

    async def stop(self):
        self.timer.stop()
        await self._chose_message.delete(reason="Draft is end")

    async def send(self, **kwargs):
        await self.ment.send(**kwargs)

    async def _send_draft_message(self) -> Message:
        embed = Embed(title="draft result", colour=Colour.brand_green())
        embed.add_field(name="🟩Your team🟩",
                        value="ban1: _ \n***pick 1: _ ***\n***pick 2: _ ***\nban2: _ \n***pick 3: _***")
        embed.add_field(name="🟥Opponent's team🟥",
                        value="ban1: _ \n***pick 1: _ ***\n***pick 2: _ ***\nban2: _ \n***pick 3: _***")
        return await self.ment.send(
            content=None,
            embed=embed
        )

    async def update_messages(self, my_character: str, opponent_character: str, *, state: str, view: View, is_final: bool):
        characters = [my_character, opponent_character]
        embed = self._draft_message.embeds[0]
        for x in 0, 1:
            embed.fields[x].value = embed.fields[x].value.replace("_", characters[x], 1)
        await self._draft_message.edit(embed=embed)
        if is_final:
            pass
        else:
            await self._chose_message.edit(
                embed=custom_embed(state == "pick", state),
                view=view
            )
