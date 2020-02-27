import pathlib
import os, re
from PIL import Image

# this class check and validate all of the user inputs to make sure the program wont fail.
# it also generate a whole lot of other important info

class UserOptions():

    gameName = ""
    gameURL = ""
    originalIconPath = ""

    steamPath = ""
    customShortcutFolder = ""

    userName = ""
    steamDirtectory = ""
    shortcutPath = ""
    gameFolderPath = ""
    vbsFile = ""
    visualElementsManifestFile = ""
    visualElementsFolder = ""
    mediumIconPath = ""
    smallIconPath = ""

    def __init__(self, gameName, gameURL, icon, steamPath, customShortcutFolder):


        #these are a few input for testing

        # ---testenin---
        # steam://rungameid/126409
        # C:\Users\Alex\Desktop\Win10-Start-menu-steam-tile-maker-master\testIcon.png
        # C:\Program Files (x86)\Steam\Steam.exe
        # C:\ProgramData\TileIconify\

        self.setGameName(gameName)
        self.setGameURL(gameURL)
        self.setOriginalIconPath(icon)
        self.setSteamPath(steamPath)
        self.setCustomShortcutFolder(customShortcutFolder)

        self.generate()

    def generate(self):
        self.steamDirtectory = "\\".join(self.steamPath.split("\\")[:-1]) + "\\"
        self.shortcutPath = os.path.join(pathlib.Path.home(), "AppData", "Roaming", "Microsoft", "Windows", "Start Menu", "Programs", "TileIconify", "Custom Shortcuts", self.gameName, self.gameName + ".lnk")
        self.gameFolderPath = os.path.join(self.setCustomShortcutFolder, self.gameName)
        self.vbsFile = os.path.join(self.gameFolderPath, self.gameName + ".vbs")
        self.visualElementsManifestFile = os.path.join(self.gameFolderPath, self.gameName + ".VisualElementsManifest.xml")
        self.visualElementsFolder = os.path.join(self.gameFolderPath, "VisualElements")
        self.mediumIconPath = os.path.join(self.visualElementsFolder, f"MediumIcon{self.gameName}.png")
        self.smallIconPath = os.path.join(self.visualElementsFolder, f"SmallIcon{self.gameName}.png")



    def setGameName(self, title):
        if(title == ""):
            raise ValueError("Invalid game title.")

        self.gameName = title



    def setGameURL(self, url):
        if(url == ""):
            raise ValueError("Invalid game url.")

        re_steamURL = re.compile("^steam://rungameid/[0-9]+$")
        if(not re_steamURL.match(url)):
            raise ValueError("Invalid game url.")

        self.gameURL = url



    def setOriginalIconPath(self, path):
        if(path == ""):
            raise ValueError("Invalid icon path.")
        if(not os.path.exists(path)):
            raise ValueError("Cannot find " + path + ".")

        try: # check if the file is valid for PILLOW
            icon = Image.open(path)
            del icon
        except OSError:
            raise ValueError("Incompatible image file.")

        self.originalIconPath = path



    def setSteamPath(self, path):
        if(path == ""):
            raise ValueError("Invalid steam path.")
        if(not os.path.exists(path)):
            raise ValueError("Cannot find " + path + ".")

        self.steamPath = path



    def setCustomShortcutFolder(self, path):
        if(path == ""):
            raise ValueError("Invalid custom shortcut path.")

        self.customShortcutFolder = path
