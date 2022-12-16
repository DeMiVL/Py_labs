from PIL import Image, ImageDraw
import sys, os
import drawlabui
from PyQt5.QtWidgets import (QMainWindow, QApplication, QScrollArea, QLabel,
                             QPushButton, QMenu, QAction, QFileDialog,
                             QLineEdit)
from PyQt5.QtGui import QPixmap, QColor, QIntValidator, QDoubleValidator, QPen, QPainter, QImage
from PyQt5.QtCore import Qt, QPoint


class PaintWindow(QMainWindow, drawlabui.Ui_MainWindow):
    def __init__(self):
        super(PaintWindow, self).__init__()
        self.setupUi(self)

        self.n = 0
        self.m = 0

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(False)

        self.editMenu = self.findChild(QMenu, "EditMenu")
        self.editMenu.setEnabled(False)

        self.actionUndo = self.findChild(QAction, "UndoAction")
        self.actionUndo.triggered.connect(self.undoAction)
        self.actionUndo.setShortcut("Ctrl+Z")

        self.actionRedo = self.findChild(QAction, "RedoAction")
        self.actionRedo.triggered.connect(self.redoAction)
        self.actionRedo.setShortcut("Ctrl+Y")
        self.actionRedo.setEnabled(False)

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

        self.actionDigit = self.findChild(QAction, "DigitAction")
        self.actionDigit.triggered.connect(self.digitAction)
        self.actionDigit.setShortcut("Ctrl+D")

        self.actionMatrix = self.findChild(QAction, "MatrixAction")
        self.actionMatrix.triggered.connect(self.matrixAction)
        self.actionMatrix.setShortcut("Ctrl+M")

        self.actionExit = self.findChild(QAction, "Exit")
        self.actionExit.triggered.connect(self.exitProg)
        self.actionExit.setShortcut("Ctrl+X")

        self.actionInputColor = self.findChild(QAction, "InputColor")
        self.actionInputColor.triggered.connect(self.inputColor)
        self.actionInputColor.setShortcut("Ctrl+I")

        self.actionFiller = self.findChild(QAction, "Filler")
        self.actionFiller.triggered.connect(self.fillEvent)
        self.actionFiller.setEnabled(False)

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

        self.drawLabel = self.findChild(QLabel, "DrawZone")
        self.drawLabel.mousePressEvent = self.doSmth
        self.drawLabel.mouseMoveEvent = self.doSmth2
        self.drawLabel.setMouseTracking(True)
        self.drawLabel.setMaximumSize(2048, 2048)
        self.drawing = False
        self.PixMapAv = False

        self.scroll.setWidget(self.drawLabel)
        self.setCentralWidget(self.scroll)

        self.nInput = QLineEdit(self)
        self.nInput.setFixedWidth(60)
        self.nInput.setFixedHeight(20)
        self.mInput = QLineEdit(self)
        self.mInput.setFixedWidth(60)
        self.mInput.setFixedHeight(20)
        self.mInput.setEnabled(False)
        self.nInput.setEnabled(False)
        self.nInput.move(470, 70)
        self.mInput.move(540, 70)
        self.mInput.setVisible(False)
        self.nInput.setVisible(False)

        self.ButtonStop = QPushButton(self)
        self.ButtonStop.move(600, 70)
        self.ButtonStop.setFixedWidth(100)
        self.ButtonStop.setFixedHeight(23)
        self.ButtonStop.clicked.connect(self.StopBut)

        self.stop = 1

        self.ButtonStop.setText("Ввод матрицы")
        self.ButtonStop.setEnabled(False)
        self.ButtonStop.setVisible(False)

        self.MatrixButton = QPushButton(self)
        self.MatrixButton.clicked.connect(self.matrixSet)
        self.MatrixButton.setText("Установить размеры")
        self.MatrixButton.move(680, 30)
        self.MatrixButton.setFixedWidth(105)
        self.MatrixButton.setFixedHeight(23)
        self.MatrixButton.setEnabled(False)
        self.MatrixButton.setVisible(False)

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

        self.BrushColor = QColor("black")
        self.BrushSize = 4
        self.FillClick = False

        self.setWindowTitle("Паинт имени Миляева Д.В.")
        self.show()


    def digitAction(self):
        ps = self.drawLabel.pixmap().copy()
        ps = ps.scaled(28, 28, aspectRatioMode = Qt.KeepAspectRatio)
        ps = ps.toImage()
        ps.save("TEst_driver_picture_temp_ultra.jpg")
        po = Image.open("TEst_driver_picture_temp_ultra.jpg")
        lo = po.load()
        a  = po.size[0]
        b  = po.size[1]
        ab = [[float(0) for i in range(a)] for j in range(b)]
        go = ImageDraw.Draw(po)
        for i in range(a):
            for j in range(b):
                R        = lo[i, j][0]
                G        = lo[i, j][1]
                B        = lo[i, j][2]
                ab[i][j] = float(R * 299/1000 + G * 587/1000 + B * 114/1000)

    def matrixAction(self):
        self.mInput.setEnabled(True)
        self.mInput.setVisible(True)
        self.nInput.setEnabled(True)
        self.nInput.setVisible(True)
        self.MatrixButton.setEnabled(True)
        self.MatrixButton.setVisible(True)

    def StopBut(self):
        self.ButtonStop.setEnabled(False)
        self.ButtonStop.setVisible(False)
        self.coercion_submission_assimilation()
        for i in range(self.n):
            for j in range(self.m):
                self.B[i][j].setVisible(False)
                self.B[i][j].setEnabled(False)
                self.layout().removeWidget(self.B[i][j])
                self.B[i][j].deleteLater()
                self.B[i][j] = None

    def matrixSet(self):
        self.MatrixButton.setEnabled(False)
        self.MatrixButton.setVisible(False)
        self.n = int(self.nInput.text())
        self.m = int(self.mInput.text())
        self.mInput.setEnabled(False)
        self.mInput.setVisible(False)
        self.nInput.setEnabled(False)
        self.nInput.setVisible(False)

        print(1)
        print(2)
        self.B = [[QLineEdit(self) for i in range(self.m)] for j in range(self.n)]
        print(3)
        for i in range(self.n):
            for j in range(self.m):
                self.B[i][j].setFixedWidth(20)
                self.B[i][j].setFixedHeight(20)
                self.B[i][j].move(80 + i * 20, 80 + j * 20)
                self.B[i][j].setValidator(QDoubleValidator(-100, 100, 2))
                self.B[i][j].setVisible(True)
                self.B[i][j].setEnabled(True)
        print(4)
        om = self.drawLabel.pixmap()  # .copy()
        # om.scaled(48, 48, Qt.KeepAspectRatio)
        im = om.toImage()
        im.save('burunya_test_drive_ultra.jpg')
        self.ButtonStop.setEnabled(True)
        self.ButtonStop.setVisible(True)

    def coercion_submission_assimilation(self):
        K1 = 0
        K2 = 0
        K3 = 0
        A = [[0 for i in range(self.m)] for j in range(self.n)]
        for i in range(self.n):
            for j in range(self.m):
                if self.B[i][j].text() == "":
                    A[i][j] = float(0)
                else:
                    A[i][j] = float(self.B[i][j].text())
        print(14)
        image = Image.open('burunya_test_drive_ultra.jpg')
        im_1 = image.load()
        weight = image.size[0]
        height = image.size[1]
        photo = Image.new(mode="RGB", size=(int(weight), int(height)))
        draw = ImageDraw.Draw(photo)
        print(weight, height)
        for k in range(weight):
            for e in range(height):
                for i in range(self.m):
                    for j in range(self.n):
                        print(k, e, i, j)
                        s = ((i - 1) / 2) * (-1)
                        t = ((j - 1) / 2) * (-1)
                        if (k + s) < 0 and (e + t) < 0:

                            x = -1 * (k + s)
                            y = -1 * (e + t)
                            K1 += im_1[x, y][0] * A[int(s)][int(t)]
                            K2 += im_1[x, y][1] * A[int(s)][int(t)]
                            K3 += im_1[x, y][2] * A[int(s)][int(t)]

                        elif (k + s) < 0 and (e + t) > 0:

                            x = -1 * (k + s)
                            K1 += im_1[x, e + t][0] * A[int(s)][int(t)]
                            K2 += im_1[x, e + t][1] * A[int(s)][int(t)]
                            K3 += im_1[x, e + t][2] * A[int(s)][int(t)]

                        elif (k + s) > 0 and (e + t) < 0:

                            y = -1 * (e + t)
                            K1 += im_1[k + s, y][0] * A[int(s)][int(t)]
                            K2 += im_1[k + s, y][1] * A[int(s)][int(t)]
                            K3 += im_1[k + s, y][2] * A[int(s)][int(t)]

                        elif (k + s) > 0 and (e + t) > 0:
                            K1 += im_1[k + s, e + t][0] * A[int(s)][int(t)]
                            K2 += im_1[k + s, e + t][1] * A[int(s)][int(t)]
                            K3 += im_1[k + s, e + t][2] * A[int(s)][int(t)]

                    if K1 > 255:
                        K1 = 255
                    if K2 > 255:
                        K2 = 255
                    if K3 > 255:
                        K3 = 255
                    if K1 < 0:
                        K1 = 0
                    if K2 < 0:
                        K2 = 0
                    if K3 < 0:
                        K3 = 0
                draw.point((k, e), (int(K1), int(K2), int(K3)))
                K1 = 0
                K2 = 0
                K3 = 0

        photo.show()
        photo.save('burunya_test_drive_ultra.jpg')
        self.pixmap = QPixmap('burunya_test_drive_ultra.jpg')
        self.drawLabel.setPixmap(self.pixmap)
        self.drawLabel.resize(self.pixmap.size())
        os.remove('burunya_test_drive_ultra.jpg')

    def openImage(self):
        filename = QFileDialog.getOpenFileName(self, "Open File", "",
                                               "All Files (*);;PNG Files (*.png);;JPG Files (*.jpg)")
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
        self.actionFiller.setEnabled(True)
        self.PixMapAv = True

    def saveImage(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save File", "./",
                                                  "PNG Files (*.png);;JPG Files (*.jpg);;ALL Files (*)")
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
        self.actionFiller.setEnabled(False)
        self.PixMapAv = False

    def exitProg(self):
        self.close()

    def fillEvent(self):
        self.FillClick = True

    def undoAction(self):
        self.actionUndo.setEnabled(False)
        pxm = QPixmap().fromImage(self.lastpxm)
        self.lastpxm = self.drawLabel.pixmap().toImage()
        self.drawLabel.setPixmap(pxm)
        self.actionRedo.setEnabled(True)

    def redoAction(self):
        self.actionRedo.setEnabled(False)
        pxm = QPixmap().fromImage(self.lastpxm)
        self.lastpxm = self.drawLabel.pixmap().toImage()
        self.drawLabel.setPixmap(pxm)
        self.actionUndo.setEnabled(True)

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
        self.actionFiller.setEnabled(True)
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
        if self.greenInput.text() == "":
            g = 0
        else:
            g = int(self.greenInput.text())
            if g > 255:
                g = 255
                self.greenInput.setText("255")
            if g < 0:
                g = 0
                self.greenInput.setText("0")
        if self.redInput.text() == "":
            r = 0
        else:
            r = int(self.redInput.text())
            if r > 255:
                r = 255
                self.redInput.setText("255")
            if r < 0:
                r = 0
                self.redInput.setText("0")
        if self.blueInput.text() == "":
            b = 0
        else:
            b = int(self.blueInput.text())
            if b > 255:
                b = 255
                self.blueInput.setText("255")
            if b < 0:
                b = 0
                self.blueInput.setText("0")

        self.BrushColor = QColor(r, g, b)
        self.greenInput.setEnabled(False)
        self.redInput.setEnabled(False)
        self.blueInput.setEnabled(False)
        self.colorButton.setEnabled(False)
        self.greenInput.setVisible(False)
        self.blueInput.setVisible(False)
        self.redInput.setVisible(False)
        self.colorButton.setVisible(False)

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
        self.redInput.setText("255")
        self.greenInput.setText("0")
        self.blueInput.setText("0")

    def bluColor(self):
        self.BrushColor = QColor("blue")
        self.blueInput.setText("255")
        self.greenInput.setText("0")
        self.redInput.setText("0")

    def grnColor(self):
        self.BrushColor = QColor("green")
        self.greenInput.setText("255")
        self.redInput.setText("0")
        self.blueInput.setText("0")

    def blkColor(self):
        self.BrushColor = QColor("black")
        self.redInput.setText("0")
        self.greenInput.setText("0")
        self.blueInput.setText("0")

    def whtColor(self):
        self.BrushColor = QColor("white")
        self.redInput.setText("255")
        self.greenInput.setText("255")
        self.blueInput.setText("255")

    def doSmth(self, event):
        if event.button() == Qt.LeftButton and not self.FillClick:
            self.actionUndo.setEnabled(True)
            self.drawing = True
            self.lastPoint = event.pos()
            pxm = self.drawLabel.pixmap()
            self.lastpxm = self.drawLabel.pixmap().toImage()
            self.editMenu.setEnabled(True)
            qp = QPainter(pxm)
            qp.setPen(QPen(self.BrushColor, self.BrushSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            qp.drawPoint(self.lastPoint)
            self.drawLabel.setPixmap(pxm)

        elif event.button() == Qt.LeftButton and self.FillClick:
            self.lastpxm = self.drawLabel.pixmap().toImage()
            self.editMenu.setEnabled(True)
            self.fillThatShit(event)
            self.FillClick = False

    def doSmth2(self, event):
        if (event.buttons() and Qt.LeftButton) and self.drawing and self.PixMapAv:
            pxm = self.drawLabel.pixmap()
            self.editMenu.setEnabled(True)
            qp = QPainter(pxm)
            qp.setPen(QPen(self.BrushColor, self.BrushSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            qp.drawLine(self.lastPoint, event.pos())
            self.lastPoint = event.pos()
            self.drawLabel.setPixmap(pxm)

    def mouseReleaseEvent(self, event):
        if event.button == Qt.LeftButton:
            self.drawing = False

    def fillThatShit(self, event):
        image = self.drawLabel.pixmap().toImage()
        w, h = image.width(), image.height()
        x, y = event.x(), event.y()
        target_color = image.pixel(x, y)

        have_seen = set()
        queue = [(x, y)]

        def get_cardinal_points(have_seen, center_pos):
            points = []
            cx, cy = center_pos
            for x, y in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                xx, yy = cx + x, cy + y
                if (xx >= 0 and xx < w and
                        yy >= 0 and yy < h and
                        (xx, yy) not in have_seen):
                    points.append((xx, yy))
                    have_seen.add((xx, yy))

            return points

        pxm = self.drawLabel.pixmap()
        p = QPainter(pxm)
        p.setPen(QPen(self.BrushColor))

        while queue:
            x, y = queue.pop()
            if image.pixel(x, y) == target_color:
                p.drawPoint(QPoint(x, y))
                queue.extend(get_cardinal_points(have_seen, (x, y)))
        self.drawLabel.setPixmap(pxm)


def main():
    app = QApplication(sys.argv)
    UIWindow = PaintWindow()
    app.exec_()


if __name__ == '__main__':
    main()