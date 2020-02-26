
# script to automate my process of making tiles for steam games


# need to create the folder for the vbs script location and the visual elements attach to it
# folder contain:
#   folder VisualElements
#   <GAMENAME>.vbs
#   <GAMENAME>.VisualElementsManifest.xml

# folder VisualElements contain:
#   <GAMENAME>.png (300x300)
#   MediumIcon<GAMENAME>_Metadata.xml
#   <GAMENAME>.png (150x150)
#   SmallIcon<GAMENAME>_Metadata.xml

# need to create a shortcut of the vbs in the tileIconify folder
# C:\Users\Pigeon\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\TileIconify\Custom Shortcuts\{gameName}\{gameName}.lnk


import os
import re
from PIL import Image

from win32com.client import Dispatch #used to create shortcut

from Config import Config

def pathExist(path):
    COLOR = "\033[94m"
    END = "\033[0m"

    if(os.path.exists(path)):
        if(os.path.isfile(path)):
            print(f"{COLOR}File{END} '{path}' {COLOR}exists.{END}")
        else:
            print(f"{COLOR}Folder{END} '{path}' {COLOR}exists.{END}")

        return True

    else:
        print(f"{COLOR}Path{END} '{path}' {COLOR}doesn't exist.{END}")
        return False



def applyConfigToData(fileData):
    
    for key in Config.__dict__:

        if(re.match("^__.*__$", key)): # ignore any magic attribute
            continue

        tag = "{" + key + "}"
        value = Config.__dict__[key]

        fileData = fileData.replace(tag, value)
    
    return fileData


def checkAndCreateGameFolder():
    gameFolderPath = Config.gameFolderPath

    if(not pathExist(gameFolderPath)):
        print("Creating...")
        os.makedirs(gameFolderPath)



def createVBS():

    vbsFile = Config.vbsFile

    if(not pathExist(vbsFile)):
        print("Creating...")

        # load template
        with open("template.vbs", "r") as f:
            vbsTemplate = f.read()

        #modify template
        vbsTemplate = applyConfigToData(vbsTemplate)

        # write vbs with modified template
        with open(vbsFile, "w") as f:
            f.write(vbsTemplate)



"""'src' is the file we want to make a shortcut of, 'dest' is the file of the shortcut we are creating wich should end with '.lnk'"""
def createShortcut(src, dest, icon=""):
    # ref: http://www.blog.pythonlibrary.org/2010/01/23/using-python-to-create-shortcuts/
    shell = Dispatch("WScript.Shell")
    shortcut = shell.createShortcut(dest)
    shortcut.Targetpath = src
    shortcut.workingDirectory = os.path.dirname(src)
    if(icon != ""):
        shortcut.IconLocation = icon

    shortcut.save()



def createVBSShortcut():
    shortcut = Config.shortcutPath
    shortcutFolder = "\\".join(shortcut.split("\\")[:-1])

    # create the shortcut folder
    if(not pathExist(shortcutFolder)):
        print("Creating...")
        os.makedirs(shortcutFolder)

    if(not pathExist(shortcut)):
        print("Creating...")
        createShortcut(Config.vbsFile, shortcut)


def createVisualElementsManifest():

    vemFile = Config.visualElementsManifestFile
    vemFolder = Config.visualElementsFolder

    if(not pathExist(vemFile)):
        print("Creating...")

        with open("template.VisualElementsManifest.xml", "r") as f:
            template = f.read()

        template = applyConfigToData(template)

        with open(vemFile, "w") as f:
            f.write(template)

    
    if(not pathExist(vemFolder)):
        print("Creating...")
        os.makedirs(vemFolder)



def createIcons():
    originalIconPath = Config.originalIconPath
    mediumIconPath = Config.mediumIconPath
    smallIconPath = Config.smallIconPath
    

    icon = Image.open(originalIconPath)

    if(not pathExist(mediumIconPath)):
        print("Creating...")
        icon.thumbnail((300,300), Image.ANTIALIAS)
        icon.save(mediumIconPath)
    
    if(not pathExist(smallIconPath)):
        print("Creating...")
        icon.thumbnail((150,150), Image.ANTIALIAS)
        icon.save(smallIconPath)

    del icon


def main():

    
    # prepare folders
    checkAndCreateGameFolder()

    # prepare the VBS file used to execute the game using the steam url
    createVBS()

    # create the shortcut in the tileIconify's shortcut folder, this is where we can pin them to the start menu
    createVBSShortcut()

    #https://docs.microsoft.com/en-us/uwp/schemas/appxpackage/uapmanifestschema/element-uap-visualelements
    #create the visual elements manifest file and prepare the folder to receive the icons
    createVisualElementsManifest()

    #create icons for the visual elements from the image specified in the configs
    createIcons()





if(__name__ == "__main__"):
    main()
