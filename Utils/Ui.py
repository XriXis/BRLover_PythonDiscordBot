from discord.ui import Button, View, button
from discord import ButtonStyle, Interaction

"""
i need take 2 groups of buttons:
    1. 3 buttons with group of characters, that return in code their label and send 2nd group of buttons
    2. 9-10 buttons with charters of chosen group and button, that return member to select group of characters
For this i need generator of button in 1 or 2 function or classes. All buttons must do equality thinks:
    "group-buttons" must generate view with "character-buttons" based on <Cogs.PickCog.lst_of_characters>
and delete the message
    "character-buttons" must disable the button and return in code their label (with <asyncio.sleep> to 
delete the message)

So i must realise system in that different buttons, that i generate (NOT CREATE) have equality (ONE) callback
And idn how to make it!

P.s.: "return in code" mean use in <Cogs.Sup.ones_choose()> or in <Cogs.DraftCog.choose()>
"""


class MyButton(Button):
    async def callback(self, interaction: Interaction):
        return self.label
