import pathlib
import os

class Config():
    
        ###        U S E D        ###

    gameName = "---testenin---"
    gameURL = "steam://rungameid/356190"
    originalIconPath = "C:\\Users\\Pigeon\\Documents\\programming\\Start menu Steam Tile maker\\Win10StartMenuSteamTileMaker\\testIcon.png"
    
    steamPath = "C:\\Program Files (x86)\\Steam\\Steam.exe"
    tileIconifyMainPath = "C:\\ProgramData\\TileIconify\\"


        ###   G E N E R A T E D   ###
    userName = str(pathlib.Path.home()).split("\\")[-1]
    steamDirtectory = "\\".join(steamPath.split("\\")[:-1]) + "\\"
    shortcutPath = os.path.join("C:\\", "Users", userName, "AppData", "Roaming", "Microsoft", "Windows", "Start Menu", "Programs", "TileIconify", "Custom Shortcuts", gameName, gameName + ".lnk")
    gameFolderPath = os.path.join(tileIconifyMainPath, gameName)
    vbsFile = os.path.join(gameFolderPath, gameName + ".vbs")
    visualElementsManifestFile = os.path.join(gameFolderPath, gameName + ".VisualElementsManifest.xml")
    visualElementsFolder = os.path.join(gameFolderPath, "VisualElements")
    mediumIconPath = os.path.join(visualElementsFolder, f"MediumIcon{gameName}.png")
    smallIconPath = os.path.join(visualElementsFolder, f"SmallIcon{gameName}.png")


