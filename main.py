
from PyQt5 import QtWidgets
import sys

from Ui import Ui



def main():

    # show ui
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    window.show()
    app.exec_()



if(__name__ == "__main__"):
    main()
    test = "test"