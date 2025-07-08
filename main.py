import sys
from GuiMainWindow import GuiMainWindow

from PySide6.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication()
    mainWindow = GuiMainWindow()
    mainWindow.show()
    sys.exit(app.exec())
