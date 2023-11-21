import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PIL import Image
import pytesseract as ts
import pyperclip


class PhotoLabel(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setAlignment(Qt.AlignCenter)
        self.setText("\n\n Drop Image Here \n\n")
        self.setStyleSheet(
            """
        QLabel {
            border: 4px dashed #aaa;
        }"""
        )

    def setPixmap(self, *args, **kwargs):
        super().setPixmap(*args, **kwargs)
        self.setStyleSheet(
            """
        QLabel {
            border: none;
        }"""
        )


class Template(QWidget):
    def __init__(self):
        super().__init__()
        self.photo = PhotoLabel()
        self.label1 = QLabel()
        btn = QPushButton("Browse")
        btn.clicked.connect(self.open_image)
        grid = QGridLayout(self)
        grid.addWidget(btn, 0, 0, Qt.AlignHCenter)
        grid.addWidget(self.label1, 1, 0)
        grid.addWidget(self.photo, 2, 0)
        self.setAcceptDrops(True)
        self.resize(300, 200)

    def dragEnterEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasImage:
            event.setDropAction(Qt.CopyAction)
            filename = event.mimeData().urls()[0].toLocalFile()
            event.accept()
            self.open_image(filename)
        else:
            event.ignore()

    def open_image(self, filename=None):
        if not filename:
            filename, _ = QFileDialog.getOpenFileName(
                self, "Select Photo", QDir.currentPath(), "Images (*.png *.jpg)"
            )
            if not filename:
                return
        self.image = Image.open(filename)
        self.photo.setPixmap(QPixmap(filename))
        self.text = self.ocr()
        self.label1.setText(self.text)

    def ocr(self):
        text = ts.image_to_string(self.image)
        pyperclip.copy(text)
        with open("output.txt", "w") as file:
            file.write(text)
        return text


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = Template()
    gui.show()
    sys.exit(app.exec_())
