
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