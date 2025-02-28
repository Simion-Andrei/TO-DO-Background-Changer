import toml
import os
class Settings():
    def __init__(self, filename):
        self.MARGIN_SIZE_X = 0.01 #This represents % of width
        self.MARGIN_SIZE_Y = 0.05 #This represents % of height
        self.COLUMNS = ["TODAY", "THIS WEEK", "NOT SO SOON"]
        self.HEADER_COLOR = (255, 255, 255)
        self.TEXT_COLOR = [(173, 0, 0), (255, 230, 0), (34, 255, 0)] #Each color coresponds to the column, same order
        self.SHADOW_COLOR = (0, 0, 0)
        self.FONT = "arial.ttf"
        self.FONT_SIZE = 0.02 #This represent % of height
        self.LINE_SPACING = 20
        
        self.__filename = filename
        self.__load_settings()

    def __load_settings(self):
        '''
        Function that loads the settings from the .toml file
        '''

        with open(self.__filename, "r") as file:
            config = toml.load(file)

        self.MARGIN_SIZE_X = config["margins"]["x"]
        self.MARGIN_SIZE_X = config["margins"]["y"]

        self.COLUMNS = config["columns"]["names"]

        self.HEADER_COLOR = tuple(config["colors"]["header"])
        self.TEXT_COLOR = [tuple(color) for color in config["colors"]["text"]]
        self.SHADOW_COLOR = tuple(config["colors"]["shadow"])

        self.FONT = config["font"]["name"]
        self.FONT_SIZE = config["font"]["size"]
        self.LINE_SPACING = config["font"]["line_spacing"]