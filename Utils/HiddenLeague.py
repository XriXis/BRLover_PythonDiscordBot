from itertools import combinations

from Utils.JsonHandler import settings


def balance(members: dict[str, int]) -> tuple[list[str], list[str]]:
    endClutch = []
    controlNum = None
    average_skill = sum(members[x] for x in members) / len(members)
    for variant in combinations(members, r=3):
        if controlNum is None:
            controlNum = abs(sum(members[x] for x in variant) - average_skill)
        elif controlNum > abs(sum(members[x] for x in variant) - average_skill):
            endClutch = variant
            controlNum = abs(sum(members[x] for x in variant) - average_skill)
    return endClutch, [x for x in members if x not in endClutch]


def convert(members: dict[str, str]) -> dict[str: int]:
    # in there must be connection to DB, but SQLHandler are empty now
    lst_of_cost = list(range(500, 3501, 500))
    result = {}
    for i in members:
        try:
            result[i] = lst_of_cost[settings["league_roles"].index(members[i])]
        except ValueError:
            result[i] = 700
    return result

# TO DO:
# 1. "new_member"
# 2. "update_league"
