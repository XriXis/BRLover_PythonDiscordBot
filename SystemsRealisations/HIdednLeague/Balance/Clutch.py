from discord import Member
from discord.ui import View

from SystemsRealisations.HIdednLeague.Balance.Balancer import Balancer
from SystemsRealisations.HIdednLeague.Balance.Ui.MemberSelectMenu import MembersSelectMenu
from SystemsRealisations.HIdednLeague.Balance.Ui.SrangersSelectMenu import StrangersSelectMenu
from Utils.MessageLib import custom_embed


class Clutch:
    def __init__(self,
                 members: list[Member],
                 channel,
                 strangers: dict[str, str]):
        self.members = members
        self.strangers = strangers
        self.channel = channel

    async def who_afk(self):
        view = View()
        view.add_item(MembersSelectMenu(self))
        await self.channel.send(
            embed=custom_embed(False, "who afk"),
            view=view
        )

    async def who_else(self):
        view = View()
        view.add_item(StrangersSelectMenu(self))
        await self.channel.send(
            embed=custom_embed(False, "who play else"),
            view=view
        )

    def exclude(self, name: str):
        if name not in [member.name for member in self.members]:
            raise AttributeError("Clutch haven't this member")
        for member in self.members:
            if name == member.name:
                break
        self.members.remove(member)

    async def start_balance(self) -> None:
        balancer = Balancer(self)
        clutch = await balancer.format_balance()
        await self.channel.send(embed=custom_embed(True, "bvm3", ", ".join(clutch[0]), ", ".join(clutch[1])),
                                delete_after=balancer.afk_time * 2)
        await balancer.next_game()
