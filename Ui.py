
from configparser import ConfigParser, NoOptionError, NoSectionError
from PyQt5 import QtWidgets, QtGui, uic
import sys, re
import pathlib
from PIL import Image
from PIL.ImageQt import ImageQt

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
        if(color != ""):
            self.inputError_label.setStyleSheet(f"color: {color};")
        else:
            self.inputError_label.setStyleSheet("")

        self.inputError_label.setText(msg)



    def setPreviewIcon(self, path):

        img = None

        try: # check if the file is valid for PILLOW
            img = Image.open(path) # load image
        except OSError:
            self.resetPreviewIcon()
            raise ValueError("Incompatible image file.")

        # need to use ImageQt to be able to open .ico files
        qimg = ImageQt(img)
        pixmap = QtGui.QPixmap.fromImage(qimg)

        # hide the border
        self.mediumIconPreview_label.setStyleSheet("")
        self.smallIconPreview_label.setStyleSheet("")

        # apply image to label
        size = (self.mediumIconPreview_label.height(), self.mediumIconPreview_label.height())
        self.mediumIconPreview_label.setPixmap(pixmap.scaled(*size))

        size = (self.smallIconPreview_label.height(), self.smallIconPreview_label.height())
        self.smallIconPreview_label.setPixmap(pixmap.scaled(*size))



    def resetPreviewIcon(self):
        self.smallIconPreview_label.setPixmap(QtGui.QPixmap())
        self.mediumIconPreview_label.setPixmap(QtGui.QPixmap())

        self.mediumIconPreview_label.setStyleSheet("border: 1px solid grey;")
        self.smallIconPreview_label.setStyleSheet("border: 1px solid grey;")



    def iconify_pushButton_clicked(self):

        self.statusMessage("Loading...")

        try:
            userOptions = UserOptions(  self.gameTitle_lineEdit.text().strip(),
                                        self.gameURL_lineEdit.text().strip(),
                                        self.iconLocation_lineEdit.text().strip(),
                                        self.steamLocation_lineEdit.text().strip(),
                                        self.customShortcutFolder_lineEdit.text().strip())

            # if everything went through, do the magic iconify stuff
            Iconify(userOptions)

            # save the settings place in steam path and custom shortcut folder
            configFileName = "config.ini"

            config = ConfigParser()
            config.read(configFileName)
            config.set("Path", "steam_path", self.steamLocation_lineEdit.text())
            config.set("Path", "custom_shortcut_folder", self.customShortcutFolder_lineEdit.text())

            with open(configFileName, "w") as configFile:
                config.write(configFile)

            self.statusMessage("Success!", "green")

        except ValueError as e:
            self.statusMessage(e.args[0], "red")



    def reset_pushButton_clicked(self):
        self.gameTitle_lineEdit.clear()
        self.gameURL_lineEdit.clear()
        self.iconLocation_lineEdit.clear()
        self.statusMessage("")
        self.resetPreviewIcon()
    


    def refresh_pushButton_clicked(self):
        # get path entered
        path = self.iconLocation_lineEdit.text()

        #if path is empty, return
        if(path == ""):
            self.statusMessage("Icon location is empty.", "red")
            return

        # try to set the preview, if fails, show error
        try:
            self.setPreviewIcon(path)
        except ValueError as e:
            self.statusMessage(e.args[0], "red")



    def gameURL_toolButton_clicked(self):
        fileName = QtWidgets.QFileDialog.getOpenFileName(self, "Open Url", "", "Internet Shortcut (*.url)")
        fileName = fileName[0] # getOpenFileName returns a tuple for some reason, I only need the path

        if(not fileName == ""):

            # get url from file
            data = ""
            with open(fileName, "r") as urlFile:
                data = urlFile.read()

            # match the url and write the result
            re_steamURL = re.compile("(?<=URL=)steam://rungameid/[0-9]+")
            match = re_steamURL.search(data)

            if(match != None):
                url = match[0]
                self.gameURL_lineEdit.setText(url)

                # set game title from the selected file
                gameTitle = pathlib.Path(fileName).stem
                self.gameTitle_lineEdit.setText(gameTitle)

                # set icon path if availlable
                if(self.iconLocation_lineEdit.text().strip() == ""): # if there is text already, don't change it

                    re_icoPath = re.compile("(?<=IconFile=).*\\.ico")
                    match = re_icoPath.search(data)

                    if(match != None):
                        path = match[0]
                        self.iconLocation_lineEdit.setText(path)
                        try:
                            self.setPreviewIcon(path)
                        except ValueError:
                            pass

            else: # if cannot find the steam game url
                self.statusMessage("Invalid game url", "red")



    def iconLocation_toolButton_clicked(self):
        fileDialogResult = QtWidgets.QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.bmp *.ico)")
        path = fileDialogResult[0] # getOpenFileName returns a path and type of file, I only need the path

        if(not path == ""):
            self.iconLocation_lineEdit.setText(path)

            try:
                self.setPreviewIcon(path)
            except ValueError as e:
                self.statusMessage(e.args[0], "red")



    def steamLocation_toolButton_clicked(self):
        fileName = QtWidgets.QFileDialog.getOpenFileName(self, "Open Steam", "", "Executable (*.exe)")
        fileName = fileName[0] # getOpenFileName returns a tuple for some reason, I only need the path

        if(not fileName == ""):
            self.steamLocation_lineEdit.setText(fileName)



    def customShortcutFolder_toolButton_clicked(self):
        folderName = QtWidgets.QFileDialog.getExistingDirectory(self, "Open Folder", "")
        if(not folderName == ""):
            self.customShortcutFolder_lineEdit.setText(folderName)



    def initUI(self):
        # apparence
        self.statusMessage("")
        self.setFixedSize(self.size())

        # set window icon
        self.setWindowIcon(QtGui.QIcon("steamIcon.ico"))

        # connections
        self.iconify_pushButton.clicked.connect(self.iconify_pushButton_clicked)
        self.reset_pushButton.clicked.connect(self.reset_pushButton_clicked)
        self.refresh_pushButton.clicked.connect(self.refresh_pushButton_clicked)

        self.gameURL_toolButton.clicked.connect(self.gameURL_toolButton_clicked)
        self.iconLocation_toolButton.clicked.connect(self.iconLocation_toolButton_clicked)
        self.steamLocation_toolButton.clicked.connect(self.steamLocation_toolButton_clicked)
        self.customShortcutFolder_toolButton.clicked.connect(self.customShortcutFolder_toolButton_clicked)



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
            self.customShortcutFolder_lineEdit.setText(config.get("Path", "custom_shortcut_folder"))
        except (NoOptionError, NoSectionError):
            pass