from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout, QScrollArea, QWidget, QGridLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class ImageGallery(QDialog):
    def __init__(self, image_paths):
        super().__init__()
        self.setWindowTitle("이미지 갤러리")
        layout = QVBoxLayout()
        scroll = QScrollArea()
        widget = QWidget()
        grid = QGridLayout()

        for i, path in enumerate(image_paths):
            pixmap = QPixmap(path).scaled(100, 100, Qt.KeepAspectRatio)
            label = QLabel()
            label.setPixmap(pixmap)
            label.mousePressEvent = lambda e, p=path: self.show_full_image(p)
            grid.addWidget(label, i // 4, i % 4)

        widget.setLayout(grid)
        scroll.setWidget(widget)
        layout.addWidget(scroll)
        self.setLayout(layout)

    def show_full_image(self, path):
        dialog = QDialog(self)
        dialog.setWindowTitle("이미지 보기")
        vbox = QVBoxLayout()
        pixmap = QPixmap(path)
        label = QLabel()
        label.setPixmap(pixmap)
        vbox.addWidget(label)
        dialog.setLayout(vbox)
        dialog.exec_()