
from PyQt5 import QtWidgets, uic
import sys

from Iconify import Iconify
from UserOptions import UserOptions

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()

        # load from the .ui file
        uic.loadUi("main.ui", self)
        
        self.initUI()

    def showError(self, msg):
        self.inputError_label.show()
        self.inputError_label.setStyleSheet("color: FireBrick;")
        self.inputError_label.setText(msg)

    def showSuccess(self):
        self.inputError_label.show()
        self.inputError_label.setStyleSheet("color: ForestGreen;")
        self.inputError_label.setText("Success!")

    def iconify_clicked(self):

        try:
            userOptions = UserOptions(  self.gameTitle_lineEdit.text(),
                                        self.gameURL_lineEdit.text(),
                                        self.iconLocation_lineEdit.text(),
                                        self.steamLocation_lineEdit.text(),
                                        self.tileIconifyFolder_lineEdit.text())

            # if everything went through, do the magic iconify stuff
            Iconify(userOptions)

            self.showSuccess()

        except ValueError as e:
            self.showError(e.args[0])

            




    def initUI(self):
        # apparence
        self.statusBar().hide()
        self.inputError_label.hide()
        width = 550
        height = 230
        self.setMinimumSize(width, height)
        self.setMaximumSize(width, height)

        # connections
        self.iconify_pushButton.clicked.connect(self.iconify_clicked)