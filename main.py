import sys
from PyQt5.QtWidgets import (QMainWindow, QApplication, QScrollArea, QLabel,
                             QPushButton, QMenu, QAction, QFileDialog,
                             QLineEdit)
from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QColor, QIntValidator, QPen, QPainter
from PyQt5.QtCore import Qt


class PaintWindow(QMainWindow):
    def __init__(self):
        super(PaintWindow, self).__init__()

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(False)

        uic.loadUi("DRAWLABUI.ui", self)

        self.brushMenu = self.findChild(QMenu, "BrushMenu")
        self.brushMenu.setEnabled(False)

        self.colorMenu = self.findChild(QMenu, "ColorMenu")
        self.colorMenu.setEnabled(False)

        self.actionNew = self.findChild(QAction, "FileAction")
        self.actionNew.triggered.connect(self.newImage)
        self.actionNew.setShortcut("Ctrl+N")

        self.actionOpen = self.findChild(QAction, "OpenAction")
        self.actionOpen.triggered.connect(self.openImage)
        self.actionOpen.setShortcut("Ctrl+O")

        self.whtAction = self.findChild(QAction, "WhiteColor")
        self.whtAction.triggered.connect(self.whtColor)
        self.redAction = self.findChild(QAction, "RedColor")
        self.redAction.triggered.connect(self.redColor)
        self.bluAction = self.findChild(QAction, "BlueColor")
        self.bluAction.triggered.connect(self.bluColor)
        self.grnAction = self.findChild(QAction, "GreenColor")
        self.grnAction.triggered.connect(self.grnColor)
        self.blkAction = self.findChild(QAction, "BlackColor")
        self.blkAction.triggered.connect(self.blkColor)

        self.actionSave = self.findChild(QAction, "SaveAction")
        self.actionSave.triggered.connect(self.saveImage)
        self.actionSave.setShortcut("Ctrl+S")

        self.actionClose = self.findChild(QAction, "CloseAction")
        self.actionClose.triggered.connect(self.closeImage)
        self.actionClose.setShortcut("Ctrl+W")

        self.actionExit = self.findChild(QAction, "Exit")
        self.actionExit.triggered.connect(self.exitProg)
        self.actionExit.setShortcut("Ctrl+X")

        self.actionInputColor = self.findChild(QAction, "InputColor")
        self.actionInputColor.triggered.connect(self.inputColor)
        self.actionInputColor.setShortcut("Ctrl+I")

        self.actionBrushSize0 = self.findChild(QAction, "BrushSize0")
        self.actionBrushSize0.triggered.connect(self.pickBrushSize0)
        self.actionBrushSize0.setEnabled(False)

        self.actionBrushSize1 = self.findChild(QAction, "BrushSize1")
        self.actionBrushSize1.triggered.connect(self.pickBrushSize1)
        self.actionBrushSize1.setEnabled(False)

        self.actionBrushSize2 = self.findChild(QAction, "BrushSize2")
        self.actionBrushSize2.triggered.connect(self.pickBrushSize2)
        self.actionBrushSize2.setEnabled(False)

        self.actionBrushSize3 = self.findChild(QAction, "BrushSize3")
        self.actionBrushSize3.triggered.connect(self.pickBrushSize3)
        self.actionBrushSize3.setEnabled(False)

        self.actionBrushSize4 = self.findChild(QAction, "BrushSize4")
        self.actionBrushSize4.triggered.connect(self.pickBrushSize4)
        self.actionBrushSize4.setEnabled(False)

        self.drawLabel  = self.findChild(QLabel, "DrawZone")
        self.drawLabel.mousePressEvent = self.doSmth
        self.drawLabel.mouseMoveEvent = self.doSmth2
        self.drawLabel.setMouseTracking(True)
        self.drawLabel.setMaximumSize(2048, 2048)
        self.drawing    = False
        self.PixMapAv   = False

        self.scroll.setWidget(self.drawLabel)
        self.setCentralWidget(self.scroll)

        self.redInput = QLineEdit(self)
        self.redInput.setFixedWidth(60)
        self.redInput.setFixedHeight(20)
        self.blueInput = QLineEdit(self)
        self.blueInput.setFixedWidth(60)
        self.blueInput.setFixedHeight(20)
        self.greenInput = QLineEdit(self)
        self.greenInput.setFixedWidth(60)
        self.greenInput.setFixedHeight(20)
        self.redInput.move(470, 30)
        self.redInput.setMaxLength(3)
        self.redInput.setValidator(QIntValidator(0, 255, self))
        self.blueInput.move(610, 30)
        self.blueInput.setMaxLength(3)
        self.blueInput.setValidator(QIntValidator(0, 255, self))
        self.greenInput.move(540, 30)
        self.greenInput.setMaxLength(3)
        self.greenInput.setValidator(QIntValidator(0, 255, self))
        self.greenInput.setEnabled(False)
        self.redInput.setEnabled(False)
        self.blueInput.setEnabled(False)

        self.colorButton = QPushButton(self)
        self.colorButton.clicked.connect(self.colorSet)
        self.colorButton.setText("Установить цвет")
        self.colorButton.move(680, 30)
        self.colorButton.setFixedWidth(95)
        self.colorButton.setFixedHeight(23)
        self.colorButton.setEnabled(False)

        self.greenInput.setVisible(False)
        self.blueInput.setVisible(False)
        self.redInput.setVisible(False)
        self.colorButton.setVisible(False)

        self.BrushColor    = QColor("red")
        self.BrushSize     = 3

        self.setWindowTitle("Паинт имени Миляева Д.В.")
        self.show()

    def openImage(self):
        filename = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*);;PNG Files (*.png);;JPG Files (*.jpg)")
        if filename == "":
            return
        self.pixmap = QPixmap(filename[0])
        self.drawLabel.setPixmap(self.pixmap)
        self.drawLabel.resize(self.pixmap.size())
        self.actionSave.setEnabled(True)
        self.actionClose.setEnabled(True)
        self.actionBrushSize0.setEnabled(True)
        self.actionBrushSize1.setEnabled(True)
        self.actionBrushSize2.setEnabled(True)
        self.actionBrushSize3.setEnabled(True)
        self.actionBrushSize4.setEnabled(True)
        self.brushMenu.setEnabled(True)
        self.colorMenu.setEnabled(True)
        self.PixMapAv = True

    def saveImage(self):
        filename, _= QFileDialog.getSaveFileName(self, "Save File", "./", "PNG Files (*.png);;JPG Files (*.jpg);;ALL Files (*)")
        if filename == "":
            return
        om = self.drawLabel.pixmap()
        im = om.toImage()
        im.save(filename)

    def closeImage(self):
        self.drawLabel.clear()
        self.drawLabel.resize(0, 0)
        self.actionSave.setEnabled(False)
        self.actionClose.setEnabled(False)
        self.actionBrushSize0.setEnabled(False)
        self.actionBrushSize1.setEnabled(False)
        self.actionBrushSize2.setEnabled(False)
        self.actionBrushSize3.setEnabled(False)
        self.actionBrushSize4.setEnabled(False)
        self.brushMenu.setEnabled(False)
        self.colorMenu.setEnabled(False)
        self.PixMapAv = False

    def exitProg(self):
        self.close()

    def newImage(self):
        self.pixmap = QPixmap(512, 512)
        self.pixmap.fill(QColor("white"))
        self.drawLabel.setPixmap(self.pixmap)
        self.drawLabel.resize(512, 512)
        self.actionSave.setEnabled(True)
        self.actionClose.setEnabled(True)
        self.actionBrushSize0.setEnabled(True)
        self.actionBrushSize1.setEnabled(True)
        self.actionBrushSize2.setEnabled(True)
        self.actionBrushSize3.setEnabled(True)
        self.actionBrushSize4.setEnabled(True)
        self.brushMenu.setEnabled(True)
        self.colorMenu.setEnabled(True)
        self.PixMapAv = True

    def inputColor(self):
        self.greenInput.setEnabled(True)
        self.redInput.setEnabled(True)
        self.blueInput.setEnabled(True)
        self.colorButton.setEnabled(True)
        self.greenInput.setVisible(True)
        self.blueInput.setVisible(True)
        self.redInput.setVisible(True)
        self.colorButton.setVisible(True)

    def colorSet(self):
        print(self.greenInput.text() == "")
        if self.greenInput.text() == "":
            g = 0
        else:
            g = int(self.greenInput.text())
            if g > 255:
                g = 255
            if g < 0:
                g = 0
        if self.redInput.text() == "":
            r = 0
        else:
            r = int(self.redInput.text())
            if r > 255:
                r = 255
            if r < 0:
                r = 0
        if self.blueInput.text() == "":
            b = 0
        else:
            b = int(self.blueInput.text())
            if b > 255:
                b = 255
            if b < 0:
                b = 0

        self.blueInput.setText("")
        self.redInput.setText("")
        self.greenInput.setText("")
        self.BrushColor = QColor(r, g, b)
        self.greenInput.setEnabled(False)
        self.redInput.setEnabled(False)
        self.blueInput.setEnabled(False)
        self.colorButton.setEnabled(False)
        self.greenInput.setVisible(False)
        self.blueInput.setVisible(False)
        self.redInput.setVisible(False)
        self.colorButton.setVisible(False)

    def mouseReleaseEvent(self, event):
        if event.button == Qt.LeftButton:
            self.drawing = False

    def pickBrushSize0(self):
        self.BrushSize = 2

    def pickBrushSize1(self):
        self.BrushSize = 4

    def pickBrushSize2(self):
        self.BrushSize = 6

    def pickBrushSize3(self):
        self.BrushSize = 8

    def pickBrushSize4(self):
        self.BrushSize = 10

    def redColor(self):
        self.BrushColor = QColor("red")

    def bluColor(self):
        self.BrushColor = QColor("blue")

    def grnColor(self):
        self.BrushColor = QColor("green")

    def blkColor(self):
        self.BrushColor = QColor("black")

    def whtColor(self):
        self.BrushColor = QColor("white")

    def doSmth(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.lastPoint = event.pos()

    def doSmth2(self, event):
        if (event.buttons() and Qt.LeftButton) and self.drawing and self.PixMapAv:
            pxm = self.drawLabel.pixmap()
            print(event.pos())
            qp  = QPainter(pxm)
            qp.setPen(QPen(self.BrushColor, self.BrushSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            qp.drawLine(self.lastPoint, event.pos())
            self.lastPoint = event.pos()
            self.drawLabel.setPixmap(pxm)


def main():
    app = QApplication(sys.argv)
    UIWindow = PaintWindow()
    app.exec_()

if __name__ == '__main__':
    main()