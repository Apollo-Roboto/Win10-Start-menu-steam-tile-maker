
from PyQt5 import QtWidgets
import sys
import platform

from Ui import Ui



def main():

    # show ui
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    window.show()
    app.exec_()



if(__name__ == "__main__"):

    # Only runs if the system is Windows
    if(platform.system() == "Windows"):
        main()
    else:
        print("Incompatible OS, this app can only run on Windows")