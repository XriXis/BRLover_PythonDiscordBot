from asyncio import sleep
from itertools import combinations

from discord import Member
from discord.ui import View

from SystemsRealisations.HIdednLeague.Balance.Ui.WinnerButton import WinnerButton
from Utils.MessageLib import custom_embed
from Utils.JsonHandler import settings, JsonHandler


class Balancer:
    def __init__(self, clutch):
        self.clutch = clutch
        self.teams: dict[str, dict[str, int]] = {}
        self.afk_time = 9 * 60

    async def format_balance(self) -> tuple[list[str], list[str]]:
        clutch = {}
        for member in self.clutch.members:
            try:
                clutch[member.name] = JsonHandler().get_score(member.id)
            except KeyError:
                try:
                    clutch[member.name] = self._convert(
                        [role.name for role in member.roles if role.name in settings["league_roles"]][0])
                except IndexError:
                    await self.clutch.channel.send(
                        embed=custom_embed(
                            False,
                            "member without role",
                            f'{member.mention}',
                            f'<@{[role.id for role in member.guild if role.name == settings["privileged_role"]][0]}>'))
                    clutch[member.name] = 500
        clutch |= {stranger: Balancer._convert(self.clutch.strangers[stranger]) for stranger in self.clutch.strangers}
        self.teams = {
            "Team1":
                {name: clutch[name] for name in list(clutch.keys())[:3]},
            "Team2":
                {name: clutch[name] for name in list(clutch.keys())[3:]}
        }
        return self._balance()

    def balance_teams(self) -> tuple[list[str], list[str]]:
        if self.teams == {}:
            raise RuntimeError("Work with teams before creating them. Call Balancer().balance() to create teams")
        else:
            return self._balance()

    def _balance(self) -> tuple[list[str], list[str]]:
        end_clutch = []
        control_num = 10 ** 10
        players = self.teams["Team1"] | self.teams["Team2"]
        average_command_skill = sum(players.values()) / 2
        for control_clutch in combinations(players, r=3):
            x = abs(sum(players[x] for x in control_clutch) - average_command_skill)
            if control_num > x:
                end_clutch = control_clutch
                control_num = x
        self.teams = {
            "Team1":
                {name: players[name] for name in end_clutch},
            "Team2":
                {name: players[name] for name in players if name not in end_clutch}
        }
        return list(self.teams["Team1"].keys()), list(self.teams["Team2"].keys())

    async def update_team_score(self, winner_team: int) -> None:
        if not self.teams:
            raise RuntimeError("Work with teams before creating them. Call Balancer().balance() to create teams")
        else:
            team_skills = [
                sum(self.teams["Team1"][player] for player in self.teams["Team1"]),
                sum(self.teams["Team2"][player] for player in self.teams["Team2"])]
            skill_difference = abs(team_skills[0] - team_skills[1])
            control_num = min(skill_difference, abs(3500 - skill_difference))
            dD = control_num if team_skills[winner_team - 1] > team_skills[1 - (winner_team - 1)] else abs(
                3500 - control_num)
            self.teams[f"Team{winner_team}"] = {
                player: self.teams[f"Team{winner_team}"][player] + dD
                for player in self.teams[f"Team{winner_team}"]
            }
            self.teams[f"Team{3 - winner_team}"] = {
                player: self.teams[f"Team{3 - winner_team}"][player] - dD
                for player in self.teams[f"Team{3 - winner_team}"]
            }
            clutch = self.teams["Team1"] | self.teams["Team2"]
            for member in self.clutch.members:
                JsonHandler().update_score(member.name, clutch[member.name])
                await self.update_member_role(member)

    async def update_member_role(self, member: Member) -> None:
        clutch = self.teams["Team1"] | self.teams["Team2"]
        member_role = [role for role in member.roles if role in settings["league_role"]][0]
        member_league = member_role.name
        role_num = (5 - settings["league_roles"].index(member_league)) * 500 + 500
        if clutch[member.name] < role_num:
            role_num -= 500
        elif clutch[member.name] >= role_num + 500 and role_num < 3500:
            role_num += 500
        else:
            return
        new_role = [role for role in member.guild.roles if role.name == settings["league_roles"][5 -
                                                                                                 (role_num // 500)]][0]
        await member.remove_roles(member_role)
        await member.add_roles(new_role)

    async def next_game(self) -> None:
        await sleep(self.afk_time)
        view = View(timeout=self.afk_time)
        for team in 1, 2, 0:
            view.add_item(WinnerButton(team, self))
        await self.clutch.channel.send(embed=custom_embed(True, "who won"), view=view)

    @staticmethod
    def _convert(role: str) -> int:
        lst_of_cost = list(range(3500, 499, -500))
        try:
            result = lst_of_cost[settings["league_roles"].index(role)]
        except ValueError:
            result = 700

        return result
