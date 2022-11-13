from discord import ButtonStyle, Interaction
from discord.ui import Button

from Utils.JsonHandler import settings
from Utils.MessageLib import custom_embed


class ActionButton(Button):
    def __init__(self, label, balancer, **kwargs):
        def smart_dict(keys, values):
            if len(keys) != len(values):
                raise AttributeError
            result = {}
            for i in range(len(keys)):
                result[keys[i]] = values[i]
            return result

        colours = smart_dict(settings["action_between_games"],
                             [ButtonStyle.green, ButtonStyle.primary, ButtonStyle.gray, ButtonStyle.red])
        super().__init__(
            label=label,
            style=colours[label],
            **kwargs
        )
        self.balancer = balancer

    async def callback(self, interaction: Interaction):
        await interaction.response.edit_message(content="ok", view=None, delete_after=1)
        match self.label:
            case "play next":
                await interaction.response.edit_message(content="ok", view=None, embed=None, delete_after=1)
                await self.balancer.next_game()
            case "rebalance":
                await interaction.response.edit_message(
                    embed=custom_embed(True,
                                       ,
                                       ", ".join(self.balancer.balance_teams()[0]),
                                       ", ".join(self.balancer.balance_teams()[1])),
                    view=None)
                await self.balancer.next_game()
            case "stop":
                await interaction.response.edit_message(content="ok", view=None, embed=None, delete_after=1)
            case _:
                pass
