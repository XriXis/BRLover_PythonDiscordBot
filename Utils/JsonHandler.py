import json
import os

JSON_DATA = os.path.dirname(os.path.abspath(__file__))[:-5] + r"Data\settings.json"

with open(JSON_DATA) as f:
    settings = json.load(f)


def change_prefix_in_data(new_prefix):
    settings['prefix'] = new_prefix
    with open(JSON_DATA, 'w') as fp:
        json.dump(settings, fp)

# TO DO: location variable
