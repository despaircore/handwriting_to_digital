import sys
from PySide6.QtWidgets import QApplication, QMainWindow

import ui_file as application_window

ui = application_window.Ui_MainWindow()

if __name__ == "__main__":
    app = QApplication([])
    window = QMainWindow()
    ui.setupUi(window)
    window.show()
    sys.exit(app.exec())
