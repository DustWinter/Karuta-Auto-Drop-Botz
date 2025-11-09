from scripts.botmanager import BotManager
from PySide6.QtWidgets import QApplication
from scripts.gui import MainWindow

if __name__ == "__main__":
    app = QApplication([])
    bot = BotManager()
    window = MainWindow()
    window.show()
    
    app.exec()
