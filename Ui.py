
from PyQt5 import QtWidgets, uic
import sys, re
import pathlib
from configparser import ConfigParser, NoOptionError, NoSectionError

from Iconify import Iconify
from UserOptions import UserOptions

class Ui(QtWidgets.QMainWindow):

    def __init__(self):
        super(Ui, self).__init__()

        # load from the .ui file
        uic.loadUi("main.ui", self)
        
        self.initUI()
        self.initFromConf()



    def statusMessage(self, msg, color=""):
        color = color.lower()
        if(color == "red"):
            self.inputError_label.setStyleSheet("color: FireBrick;")
        elif(color == "green"):
            self.inputError_label.setStyleSheet("color: ForestGreen;")
        else:
            self.inputError_label.setStyleSheet("")

        self.inputError_label.setText(msg)

    def iconify_pushButton_clicked(self):

        try:
            userOptions = UserOptions(  self.gameTitle_lineEdit.text(),
                                        self.gameURL_lineEdit.text(),
                                        self.iconLocation_lineEdit.text(),
                                        self.steamLocation_lineEdit.text(),
                                        self.tileIconifyFolder_lineEdit.text())

            # if everything went through, do the magic iconify stuff
            Iconify(userOptions)

            # save the settings place in steam path and custom shortcut folder
            configFileName = "config.ini"

            config = ConfigParser()
            config.read(configFileName)
            config.set("Path", "steam_path", self.steamLocation_lineEdit.text())
            config.set("Path", "custom_shortcut_folder", self.tileIconifyFolder_lineEdit.text())

            with open(configFileName, "w") as configFile:
                config.write(configFile)

            self.statusMessage("Success!", "green")

        except ValueError as e:
            self.statusMessage(e.args[0], "red")



    def gameURL_toolButton_clicked(self):
        # fileName = QtWidgets.QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.bmp)")
        # print(fileName[0])

        fileName = QtWidgets.QFileDialog.getOpenFileName(self, "Open Url", "", "Internet Shortcut (*.url)")
        fileName = fileName[0] # getOpenFileName returns a tuple for some reason, I only need the path

        if(not fileName == ""):

            # get url from file
            data = ""
            with open(fileName, "r") as urlFile:
                data = urlFile.read()

            # match the url and write the result
            re_steamURL = re.compile("steam://rungameid/[0-9]+")
            match = re_steamURL.search(data)

            if(match != None):
                url = match[0]
                self.gameURL_lineEdit.setText(url)

                # set game title from the selected file
                gameTitle = pathlib.Path(fileName).stem
                self.gameTitle_lineEdit.setText(gameTitle)

            else:
                self.statusMessage("Invalid game url", "red")


    def iconLocation_toolButton_clicked(self):

        fileName = QtWidgets.QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.bmp)")
        fileName = fileName[0] # getOpenFileName returns a tuple for some reason, I only need the path

        if(not fileName == ""):
            #todo update preview icon from there
            self.iconLocation_lineEdit.setText(fileName)



    def steamLocation_toolButton_clicked(self):
        fileName = QtWidgets.QFileDialog.getOpenFileName(self, "Open Steam", "", "Executable (*.exe)")
        fileName = fileName[0] # getOpenFileName returns a tuple for some reason, I only need the path

        if(not fileName == ""):
            self.steamLocation_lineEdit.setText(fileName)



    def tileIconifyFolder_toolButton_clicked(self):
        folderName = QtWidgets.QFileDialog.getExistingDirectory(self, "Open Folder", "")
        if(not folderName == ""):
            self.tileIconifyFolder_lineEdit.setText(folderName)



    def initUI(self):
        # apparence
        self.statusBar().hide()
        self.inputError_label.setText("")
        width = 600
        height = 300
        self.setMinimumSize(width, height)
        self.setMaximumSize(width, height)

        # connections
        self.iconify_pushButton.clicked.connect(self.iconify_pushButton_clicked)

        self.gameURL_toolButton.clicked.connect(self.gameURL_toolButton_clicked)
        self.iconLocation_toolButton.clicked.connect(self.iconLocation_toolButton_clicked)
        self.steamLocation_toolButton.clicked.connect(self.steamLocation_toolButton_clicked)
        self.tileIconifyFolder_toolButton.clicked.connect(self.tileIconifyFolder_toolButton_clicked)



    def initFromConf(self):
        # read from config file
        configFileName = "config.ini"

        config = ConfigParser()
        config.read(configFileName)

        try: # try to get steam_path from config file
            self.steamLocation_lineEdit.setText(config.get("Path", "steam_path"))
        except (NoOptionError, NoSectionError):
            pass

        try: # try to get custom_shortcut_folder from config file
            self.tileIconifyFolder_lineEdit.setText(config.get("Path", "custom_shortcut_folder"))
        except (NoOptionError, NoSectionError):
            pass


        
        
