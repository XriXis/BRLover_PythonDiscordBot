from discord import ButtonStyle
from discord.ui import Button

from Utils.JsonHandler import lst_of_characters
from SystemsRealisations.DraftSystem.Captain import Captain


class BaseButton(Button):
    def __init__(self, label, capitan: Captain, draft, **kwargs):
        colour = self.get_colour_by_button(label)
        super().__init__(label=label, style=colour, **kwargs)
        self.captain = capitan
        self.draft = draft

    @staticmethod
    def get_colour_by_button(label):
        if label in lst_of_characters:
            group = label
        else:
            group = [[x for x in lst_of_characters if label in lst_of_characters[x]] + [None]][0][0]

        match group:
            case "melee":
                colour = ButtonStyle.red
            case "range":
                colour = ButtonStyle.primary  # blue
            case "supports":
                colour = ButtonStyle.success  # green
            case _:
                colour = ButtonStyle.gray
        return colour
