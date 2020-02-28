import os, re
from win32com.client import Dispatch #used to create shortcut
from PIL import Image
import pathlib

from UserOptions import UserOptions

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



class Iconify:

    userOptions = None



    def __init__(self, userOptions):

        # check if userOptions is valid
        if(not isinstance(userOptions, UserOptions)):
            raise ValueError("invalid UserOptions")

        self.userOptions = userOptions

        # prepare folders
        self.checkAndCreateGameFolder()

        # prepare the VBS file used to execute the game using the steam url
        self.createVBS()

        # create the shortcut in the tileIconify's shortcut folder, this is where we can pin them to the start menu
        self.createVBSShortcut()

        #https://docs.microsoft.com/en-us/uwp/schemas/appxpackage/uapmanifestschema/element-uap-visualelements
        #create the visual elements manifest file and prepare the folder to receive the icons
        self.createVisualElementsManifest()

        #create icons for the visual elements from the image specified in the configs
        self.createIcons()

        self.createIconMetadata()

        print("\033[92mSuccess!\033[0m")



    def applyUserOptionsToData(self, fileData):
        
        for key in self.userOptions.__dict__:

            if(re.match("^__.*__$", key)): # ignore any magic attribute
                continue

            tag = "{" + key + "}"
            value = self.userOptions.__dict__[key]

            fileData = fileData.replace(tag, value)
        
        return fileData



    def checkAndCreateGameFolder(self):
        gameFolderPath = self.userOptions.gameFolderPath

        if(not pathExist(gameFolderPath)):
            print("Creating...")
            os.makedirs(gameFolderPath)



    def createVBS(self):

        vbsFile = self.userOptions.vbsFile

        if(not pathExist(vbsFile)):
            print("Creating...")

            # load template
            with open("templates/template.vbs", "r") as f:
                vbsTemplate = f.read()

            #modify template
            vbsTemplate = self.applyUserOptionsToData(vbsTemplate)

            # write vbs with modified template
            with open(vbsFile, "w") as f:
                f.write(vbsTemplate)



    def createVBSShortcut(self):
        shortcut = self.userOptions.shortcutPath
        shortcutFolder = "\\".join(shortcut.split("\\")[:-1])

        # create the shortcut folder
        if(not pathExist(shortcutFolder)):
            print("Creating...")
            os.makedirs(shortcutFolder)

        if(not pathExist(shortcut)):
            print("Creating...")
            createShortcut(self.userOptions.vbsFile, shortcut)



    def createVisualElementsManifest(self):

        vemFile = self.userOptions.visualElementsManifestFile
        vemFolder = self.userOptions.visualElementsFolder

        if(not pathExist(vemFile)):
            print("Creating...")

            with open("templates/template.VisualElementsManifest.xml", "r") as f:
                template = f.read()

            template = self.applyUserOptionsToData(template)

            with open(vemFile, "w") as f:
                f.write(template)
        
        if(not pathExist(vemFolder)):
            print("Creating...")
            os.makedirs(vemFolder)



    def createIcons(self):
        originalIconPath = self.userOptions.originalIconPath
        mediumIconPath = self.userOptions.mediumIconPath
        smallIconPath = self.userOptions.smallIconPath

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


    # tileIconifier need those metadata file
    def createIconMetadata(self):
        mediumIconPath = self.userOptions.mediumIconPath
        smallIconPath = self.userOptions.smallIconPath

        mediumIconMeta = pathlib.Path(mediumIconPath).stem
        smalIconMeta = pathlib.Path(smallIconPath).stem

        #whereiwas make the metadata file tileiconifier uses

        pass