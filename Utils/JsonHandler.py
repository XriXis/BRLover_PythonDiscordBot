import json
import os


class JsonHandler:
    PATH = os.path.dirname(os.path.abspath(__file__))[:-5] + r"Data\state_of_everyone.json"
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        with open(self.PATH, encoding="utf-8") as st:
            self.state = json.load(st)

    def get_score(self, member_id: int) -> int:
        return self.state[member_id][1]

    def update_score(self, name: str, new_score: int) -> None:
        ok = False
        for id_ in self.state:
            if self.state[id_][0] == name:
                ok = True
                break
        if ok:
            self.state[id_][1] = new_score
            with open(self.PATH, "w", encoding="utf-8") as st:
                json.dump(self.state, st)
        else:
            raise AttributeError(f"Unknown name {name}. Use JsonHandler().new_member(<id>, {name}, {new_score}) before")

    def new_member(self, id_: int, name: str, score: int) -> None:
        self.state[id_] = [name, score]
        with open(self.PATH, encoding="utf-8") as st:
            json.dump(self.state, st)


JSON_META_DATA_PATH = os.path.dirname(os.path.abspath(__file__))[:-5] + r"Data\bot_meta_data.json"
LOCALISATION_PATH = os.path.dirname(os.path.abspath(__file__))[:-5] + r"Languages\%s.json"
JSON_GUILd_SETTINGS_PATH = os.path.dirname(os.path.abspath(__file__))[:-5] + r"Data\guild_settings\{0}.json"

with open(JSON_META_DATA_PATH, encoding="utf-8") as sett:
    meta_data = json.load(sett)
    settings = json.load(sett)

with open(LOCALISATION_PATH % settings["lang"], encoding="utf-8") as lang_fp:
    message_texts = json.load(lang_fp)

guild_settings = {}


def generate_current_settings(guild_id: int) -> None:
    global settings
    global guild_settings
    with open(JSON_GUILd_SETTINGS_PATH.format(guild_id), 'r', encoding="utf-8") as fp:
        guild_settings = json.load(fp)
    settings = meta_data | guild_settings


def add_guild_settings(guild_id: int,
                       privileged_role_id:int,
                       game_roles: dict[str, str],
                       league_roles: list[str]) -> None:
    with open(JSON_GUILd_SETTINGS_PATH.format(guild_id), 'w', encoding="utf-8") as fp:
        json.dump(
            {
                "prefix": "=",
                "privileged role": privileged_role_id,
                "lang": "ENG",
                "time_to_draft_phase_in_seconds": 300,
                "league_roles": league_roles,
                "game_roles": game_roles
            }, fp)


def change_lang_in_data(new_lang: str, guild_id) -> None:
    global message_texts
    guild_settings['lang'] = new_lang
    with open(JSON_GUILd_SETTINGS_PATH.format(guild_id), 'w', encoding="utf-8") as fp:
        json.dump(guild_settings, fp)
    with open(LOCALISATION_PATH % settings["lang"], encoding="utf-8") as f:
        message_texts = json.load(f)


def change_prefix_in_data(new_prefix, guild_id):
    guild_settings['prefix'] = new_prefix
    with open(JSON_GUILd_SETTINGS_PATH.format(guild_id), 'w', encoding="utf-8") as fp:
        json.dump(settings, fp)


lst_of_characters = {
    "melee": ["Bakko", "Croak", "Freya", "Jamila", "Raigon", "Rook", "Ruh Kaan", "Shifu", "Thorn"],
    "range": ['Ashka', 'Alysia', 'Desteny', 'Ezmo', 'Iva', 'Jade', 'Jumong', 'Shen Rao', 'Taya', 'Varesh'],
    "supports": ['Blossom', 'Lucie', 'Oldur', 'Perl', 'Pestilus', 'Poloma', 'Sirius', 'Ulric', 'Zander']
}
