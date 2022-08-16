import json
import os

JSON_DATA = os.path.dirname(os.path.abspath(__file__))[:-5] + r"Data\settings.json"
LANG = os.path.dirname(os.path.abspath(__file__))[:-5] + r"Languages\%s.json"

with open(JSON_DATA, encoding="utf-8") as sett:
    settings = json.load(sett)

with open(LANG % settings["lang"], encoding="utf-8") as lang_fp:
    message_texts = json.load(lang_fp)


def change_lang_in_data(new_lang: str) -> None:
    global message_texts
    settings['lang'] = new_lang
    with open(JSON_DATA, 'w', encoding="utf-8") as fp:
        json.dump(settings, fp)
    with open(LANG % settings["lang"], encoding="utf-8") as f:
        message_texts = json.load(f)


def change_prefix_in_data(new_prefix):
    settings['prefix'] = new_prefix
    with open(JSON_DATA, 'w', encoding="utf-8") as fp:
        json.dump(settings, fp)
