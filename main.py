from PyQt5.QtWidgets import QApplication
from ui import ImageGeneratorApp
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageGeneratorApp()
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec_())