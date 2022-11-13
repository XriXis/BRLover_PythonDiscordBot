from discord import Interaction
from discord.ui import Button, View

from SystemsRealisations.HIdednLeague.Balance.Ui.ActionButton import ActionButton
from Utils.JsonHandler import settings
from Utils.MessageLib import custom_embed


class WinnerButton(Button):
    def __init__(self, team, balancer, **kwargs):
        super().__init__(
            label=f"Team {team}" if team != 0 else "No one (had troubles)",
            emoji="🟩" if team == 1 else "🟥" if team == 2 else "✖",
            **kwargs
        )
        self.team = team
        self.balancer = balancer

    async def callback(self, interaction: Interaction):
        if self.team != 0:
            await self.balancer.update_team_score(self.team)
        view = View()
        for action in settings["action_between_games"]:
            view.add_item(ActionButton(action, self.balancer))
        await interaction.response.edit_message(
            embed=custom_embed(True, "what next"),
            view=view
        )


