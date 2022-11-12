from ctypes import Union
from itertools import combinations

from discord import Member

from Utils.JsonHandler import settings
from Utils.SQLHandler import SQLHandler


class Balancer:
    def __init__(self, clutch):
        self.clutch = clutch
        self.teams: dict[Union("Team1", "Team2"), dict[str, int]] = {}

    def balance(self) -> tuple[list[str], list[str]]:
        end_clutch = []
        control_num = -1
        clutch = {member.name: SQLHandler.get_score(member.id) for member in self.clutch.members}
        for stranger in self.clutch.strangers:
            clutch[Balancer._stranger_name(stranger, clutch)] = Balancer.convert(stranger)
        average_command_skill = sum(clutch.values()) / 2
        for control_clutch in combinations(clutch, r=3):
            x = abs(sum(clutch[x] for x in control_clutch) - average_command_skill)
            if control_num < x:
                end_clutch = control_clutch
                control_num = x
        self.teams = {
            "Team1":
                {name: clutch[name] for name in end_clutch},
            "Team2":
                {name: clutch[name] for name in clutch if name not in end_clutch}
        }
        return list(self.teams["Team1"].keys()), list(self.teams["Team2"].keys())

    @staticmethod
    def convert(role: str) -> int:
        lst_of_cost = list(range(500, 3501, 500))
        try:
            result = lst_of_cost[settings["league_roles"].index(role)]
        except ValueError:
            result = 700

        return result

    @staticmethod
    def _stranger_name(league: str, clutch: dict[str, int], _index=1) -> str:
        name = f"{league}{_index} player"
        if name not in clutch:
            return name
        else:
            return Balancer._stranger_name(league, clutch, _index + 1)
