from PIL import Image, ImageDraw
import sys, os, random
import drawlabui

from   PyQt5.QtWidgets  import(QMainWindow, QApplication, QScrollArea, QLabel,
                               QPushButton, QMenu, QAction, QFileDialog,
                               QLineEdit)
from   PyQt5.QtGui      import QPixmap, QColor, QIntValidator, QDoubleValidator, QPen, QPainter, QImage, QFont
from   PyQt5.QtCore     import Qt, QPoint

#from keras.models import load_model
#import keras.utils

#def minvalue(list):
#    min_val = max(list)
#    min_ind = list.index(min_val)
#    return min_ind

class PaintWindow(QMainWindow, drawlabui.Ui_MainWindow):
    def __init__(self):
        super(PaintWindow, self).__init__()
        self.setupUi(self)

        self.n = 0
        self.m = 0

        self.scroll      = QScrollArea()
        self.scroll.setWidgetResizable(False)

        self.editMenu    = self.findChild(QMenu, "EditMenu")
        self.editMenu.setEnabled(False)

        self.actionUndo  = self.findChild(QAction, "UndoAction")
        self.actionUndo.triggered.connect(self.undoAction)
        self.actionUndo.setShortcut("Ctrl+Z")

        self.actionRedo  = self.findChild(QAction, "RedoAction")
        self.actionRedo.triggered.connect(self.redoAction)
        self.actionRedo.setShortcut("Ctrl+Y")
        self.actionRedo.setEnabled(False)

        self.actionSP    = self.findChild(QAction, "Sepiaaction")
        self.actionBW    = self.findChild(QAction, "BWACT")
        self.actionGS    = self.findChild(QAction, "GSACT")
        self.actionNS    = self.findChild(QAction, "NOISEACT")
        self.actionNG    = self.findChild(QAction, "NEGACT")

        self.actionSP.triggered.connect(self.sepiaAction)
        self.actionBW.triggered.connect(self.bwAction)
        self.actionGS.triggered.connect(self.gsAction)
        self.actionNS.triggered.connect(self.nsAction)
        self.actionNG.triggered.connect(self.ngAction)

        self.brushMenu   = self.findChild(QMenu, "BrushMenu")
        self.brushMenu.setEnabled(False)

        self.colorMenu   = self.findChild(QMenu, "ColorMenu")
        self.colorMenu.setEnabled(False)

        self.actionNew   = self.findChild(QAction, "FileAction")
        self.actionNew.triggered.connect(self.newImage)
        self.actionNew.setShortcut("Ctrl+N")

        self.actionOpen  = self.findChild(QAction, "OpenAction")
        self.actionOpen.triggered.connect(self.openImage)
        self.actionOpen.setShortcut("Ctrl+O")

        self.whtAction   = self.findChild(QAction, "WhiteColor")
        self.whtAction.triggered.connect(self.whtColor)
        self.redAction   = self.findChild(QAction, "RedColor")
        self.redAction.triggered.connect(self.redColor)
        self.bluAction   = self.findChild(QAction, "BlueColor")
        self.bluAction.triggered.connect(self.bluColor)
        self.grnAction   = self.findChild(QAction, "GreenColor")
        self.grnAction.triggered.connect(self.grnColor)
        self.blkAction   = self.findChild(QAction, "BlackColor")
        self.blkAction.triggered.connect(self.blkColor)

        self.actionSave  = self.findChild(QAction, "SaveAction")
        self.actionSave.triggered.connect(self.saveImage)
        self.actionSave.setShortcut("Ctrl+S")

        self.actionClose = self.findChild(QAction, "CloseAction")
        self.actionClose.triggered.connect(self.closeImage)
        self.actionClose.setShortcut("Ctrl+W")

        self.actionMatrix = self.findChild(QAction, "MatrixAction")
        self.actionMatrix.triggered.connect(self.matrixAction)
        self.actionMatrix.setShortcut("Ctrl+M")

        self.actionExit = self.findChild(QAction, "Exit")
        self.actionExit.triggered.connect(self.exitProg)
        self.actionExit.setShortcut("Ctrl+X")

        self.actionInputColor = self.findChild(QAction, "InputColor")
        self.actionInputColor.triggered.connect(self.inputColor)
        self.actionInputColor.setShortcut("Ctrl+I")

        self.actionFiller     = self.findChild(QAction, "Filler")
        self.actionFiller.triggered.connect(self.fillEvent)
        self.actionFiller.setEnabled(False)

        #self.digitAction = self.findChild(QAction, "DigitAction")
        #self.digitAction.triggered.connect(self.digitEvent)

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

        self.AddImages = self.findChild(QAction, "ActAddIm")
        self.AddImages.triggered.connect(self.AddPictures)

        self.SubImages = self.findChild(QAction, "ActSubIM")
        self.SubImages.triggered.connect(self.SubPictures)

        self.DivImages = self.findChild(QAction, "actionDIvIms")
        self.DivImages.triggered.connect(self.DivPictures)

        self.MulImages = self.findChild(QAction, "actionMulIMs")
        self.MulImages.triggered.connect(self.MulPictures)

        self.TextAdd = self.findChild(QAction, "action_text")
        self.TextAdd.triggered.connect(self.AddText)

        self.drawLabel  = self.findChild(QLabel, "DrawZone")
        self.drawLabel.mousePressEvent = self.doSmth
        self.drawLabel.mouseMoveEvent  = self.doSmth2
        self.drawLabel.setMouseTracking(True)
        self.drawLabel.setMaximumSize(2048, 2048)
        self.drawing    = False
        self.PixMapAv   = False

        self.scroll.setWidget(self.drawLabel)
        self.setCentralWidget(self.scroll)

        self.nInput  = QLineEdit(self)
        self.nInput.setFixedWidth(60)
        self.nInput.setFixedHeight(20)
        self.mInput  = QLineEdit(self)
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

        self.redInput   = QLineEdit(self)
        self.redInput.setFixedWidth(60)
        self.redInput.setFixedHeight(20)
        self.blueInput  = QLineEdit(self)
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

        self.BrushColor  = QColor("black")
        self.BrushSize   = 4
        self.FillClick   = False
        
        #self.model = load_model('NeuronNet.h5')
        
        self.setWindowTitle("Паинт имени Миляева Д.В.")
        self.show()

    def AddLine(self):
        text = self.Text.text()
        x    = int(self.X_1.text())
        y    = int(self.Y_1.text())
        fs   = int(self.FontSize.text())
        self.layout().removeWidget(self.Text)
        self.Text.deleteLater()
        self.Text = None
        self.layout().removeWidget(self.FontSize)
        self.FontSize.deleteLater()
        self.FontSize = None
        self.layout().removeWidget(self.textButton)
        self.textButton.deleteLater()
        self.textButton = None
        self.layout().removeWidget(self.X_1)
        self.X_1.deleteLater()
        self.X_1 = None
        self.layout().removeWidget(self.Y_1)
        self.Y_1.deleteLater()
        self.Y_1 = None
        pxm = self.drawLabel.pixmap()
        paint = QPainter(pxm)
        paint.setPen(QPen(self.BrushColor, 1, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        paint.setFont(QFont("Arial", fs))
        paint.drawText(x, y, text)
        self.drawLabel.setPixmap(pxm)

    def AddText(self):
        self.X_1  = QLineEdit(self)
        self.Y_1  = QLineEdit(self)
        self.Text = QLineEdit(self)
        self.X_1.setValidator(QIntValidator(0, self.drawLabel.width()))
        self.Y_1.setValidator(QIntValidator(0, self.drawLabel.height()))
        self.X_1.setVisible(True)
        self.FontSize = QLineEdit(self)
        self.FontSize.setVisible(True)
        self.FontSize.move(600, 40)
        self.FontSize.setFixedHeight(40)
        self.FontSize.setFixedWidth(60)
        self.X_1.move(600, 80)
        self.Y_1.move(600, 160)
        self.Text.move(600, 240)
        self.X_1.setFixedHeight(40)
        self.X_1.setFixedWidth(60)
        self.Y_1.setFixedHeight(40)
        self.Y_1.setFixedWidth(60)
        self.Text.setFixedHeight(40)
        self.Text.setFixedWidth(240)
        self.Y_1.setVisible(True)
        self.Text.setVisible(True)
        self.textButton = QPushButton(self)
        self.textButton.move(600, 300)
        self.textButton.setFixedHeight(40)
        self.textButton.setFixedWidth(240)
        self.textButton.setText('Ввод строки')
        self.textButton.setVisible(True)
        self.textButton.clicked.connect(self.AddLine)

    def AddPictures(self):
        filename = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*);;PNG Files (*.png);;JPG Files (*.jpg)")
        if filename == "":
            return
        pxm1 = self.drawLabel.pixmap()
        pxm2  = QPixmap(filename[0])
        if pxm1.height() != pxm2.height() or pxm1.width() != pxm2.width():
            print("Sizes are not equal")
            return
        im  = pxm1.toImage()
        im2 = pxm2.toImage()
        a   = pxm1.width()
        b   = pxm1.height()
        qp  = QPainter(pxm1)
        for i in range(a):
            for j in range(b):
                colord = im.pixel(i, j)
                colorp = im2.pixel(i, j)
                colorm = QColor(colord).getRgb()
                colort = QColor(colorp).getRgb()
                R = colorm[0] + colort[0]
                G = colorm[1] + colort[1]
                B = colorm[2] + colort[2]
                if R > 255:
                    R = 255
                if G > 255:
                    G = 255
                if B > 255:
                    B = 255
                if R < 0:
                    R = 0
                if G < 0:
                    G = 0
                if B < 0:
                    B = 0
                qp.setPen(QPen(QColor(R, G, B), 1, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
                qp.drawPoint(i, j)
        self.drawLabel.setPixmap(pxm1)
    
    def SubPictures(self):
        filename = QFileDialog.getOpenFileName(self, "Open File", "",
                                               "All Files (*);;PNG Files (*.png);;JPG Files (*.jpg)")
        if filename == "":
            return
        pxm1 = self.drawLabel.pixmap()
        pxm2 = QPixmap(filename[0])
        if pxm1.height() != pxm2.height() or pxm1.width() != pxm2.width():
            print("Sizes are not equal")
            return
        im = pxm1.toImage()
        im2 = pxm2.toImage()
        a = pxm1.width()
        b = pxm1.height()
        qp = QPainter(pxm1)
        for i in range(a):
            for j in range(b):
                colord = im.pixel(i, j)
                colorp = im2.pixel(i, j)
                colorm = QColor(colord).getRgb()
                colort = QColor(colorp).getRgb()
                R = colorm[0] - colort[0]
                G = colorm[1] - colort[1]
                B = colorm[2] - colort[2]
                if R > 255:
                    R = 255
                if G > 255:
                    G = 255
                if B > 255:
                    B = 255
                if R < 0:
                    R = 0
                if G < 0:
                    G = 0
                if B < 0:
                    B = 0
                qp.setPen(QPen(QColor(R, G, B), 1, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
                qp.drawPoint(i, j)
        self.drawLabel.setPixmap(pxm1)
    
    def DivPictures(self):
        filename = QFileDialog.getOpenFileName(self, "Open File", "",
                                               "All Files (*);;PNG Files (*.png);;JPG Files (*.jpg)")
        if filename == "":
            return
        pxm1 = self.drawLabel.pixmap()
        pxm2 = QPixmap(filename[0])
        if pxm1.height() != pxm2.height() or pxm1.width() != pxm2.width():
            print("Sizes are not equal")
            return
        im = pxm1.toImage()
        im2 = pxm2.toImage()
        a = pxm1.width()
        b = pxm1.height()
        qp = QPainter(pxm1)
        for i in range(a):
            for j in range(b):
                colord = im.pixel(i, j)
                colorp = im2.pixel(i, j)
                colorm = QColor(colord).getRgb()
                colort = QColor(colorp).getRgb()
                R = int((colorm[0] + 1)/ (colort[0] + 1) - 1)
                G = int((colorm[1] + 1)/ (colort[1] + 1) - 1)
                B = int((colorm[2] + 1)/ (colort[2] + 1) - 1)
                if R > 255:
                    R = 255
                if G > 255:
                    G = 255
                if B > 255:
                    B = 255
                if R < 0:
                    R = 0
                if G < 0:
                    G = 0
                if B < 0:
                    B = 0
                qp.setPen(QPen(QColor(R, G, B), 1, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
                qp.drawPoint(i, j)
        self.drawLabel.setPixmap(pxm1)
    
    def MulPictures(self):
        filename = QFileDialog.getOpenFileName(self, "Open File", "",
                                               "All Files (*);;PNG Files (*.png);;JPG Files (*.jpg)")
        if filename == "":
            return
        pxm1 = self.drawLabel.pixmap()
        pxm2 = QPixmap(filename[0])
        if pxm1.height() != pxm2.height() or pxm1.width() != pxm2.width():
            print("Sizes are not equal")
            return
        im = pxm1.toImage()
        im2 = pxm2.toImage()
        a = pxm1.width()
        b = pxm1.height()
        qp = QPainter(pxm1)
        for i in range(a):
            for j in range(b):
                colord = im.pixel(i, j)
                colorp = im2.pixel(i, j)
                colorm = QColor(colord).getRgb()
                colort = QColor(colorp).getRgb()
                R = int(colorm[0] * colort[0] / 255)
                G = int(colorm[1] * colort[1] / 255)
                B = int(colorm[2] * colort[2] / 255)
                if R > 255:
                    R = 255
                if G > 255:
                    G = 255
                if B > 255:
                    B = 255
                if R < 0:
                    R = 0
                if G < 0:
                    G = 0
                if B < 0:
                    B = 0
                qp.setPen(QPen(QColor(R, G, B), 1, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
                qp.drawPoint(i, j)
        self.drawLabel.setPixmap(pxm1)
    
    def antiDigitEvent(self):
        self.layout().removeWidget(self.digitAnti)
        self.digitAnti.deleteLater()
        self.digitAnti = None
        self.layout().removeWidget(self.digitLabel)
        self.digitLabel.deleteLater()
        self.digitLabel = None

    def digitEvent(self):
        pxm   = self.drawLabel.pixmap().copy()
        pxm   = pxm.scaled(28, 28)
        im    = pxm.toImage()
        im.save("Slovo.jpg", "JPG")
        im    = Image.open("Slovo.jpg")
        im_ar = keras.utils.img_to_array(im)
        im_ar = im_ar[:, :, 0]
        im_ar = im_ar.reshape((1, 28 * 28))
        im_ar = im_ar.astype('float32') / 255
        train_images = [im_ar]
        ints  = self.model.predict(train_images)
        into  = len(ints[0])
        p     = list()

        for i in range(into):
            p.append(ints[0][i])

        m     = minvalue(p)
        self.digitLabel = QLabel(self)
        self.digitLabel.setFixedWidth(60)
        self.digitLabel.setFixedHeight(60)
        self.digitLabel.setVisible(True)
        self.digitLabel.setText(str(m))
        self.digitLabel.move(700, 300)
        self.digitAnti = QPushButton(self)
        self.digitAnti.setFixedWidth(80)
        self.digitAnti.setFixedHeight(20)
        self.digitAnti.setVisible(True)
        self.digitAnti.move(700, 380)
        self.digitAnti.setText("Убрать цифру")
        self.digitAnti.clicked.connect(self.antiDigitEvent)
        print(m)

    def sepiaAcTAction(self):
        if self.GSFACTORINPUT.text() == "":
            factor = 1
        else:
            factor = float(self.GSFACTORINPUT.text()) / 100
        if factor > 1:
            factor = 1
        if factor < 0:
            factor = 1
        self.layout().removeWidget(self.GSFACTORINPUT)
        self.GSFACTORINPUT.deleteLater()
        self.GSFACTORINPUT = None
        self.layout().removeWidget(self.GSBUTTON)
        self.GSBUTTON.deleteLater()
        self.GSBUTTON = None
        pxm = self.drawLabel.pixmap()
        im  = pxm.toImage()
        a   = pxm.width()
        b   = pxm.height()
        qp  = QPainter(pxm)
        for i in range(a):
            for j in range(b):
                colord = im.pixel(i, j)
                colorm = QColor(colord).getRgb()
                R = colorm[0]
                G = colorm[1]
                B = colorm[2]
                C = int((0.3 * R) + (0.59 * G) + (0.11 * B))
                if C > 255:
                    C == 255
                qp.setPen(QPen(QColor(int(C * factor + (1 - factor) * R), int(C * factor + (1 - factor) * G), int(C * factor + (1 - factor) * B)), 1, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
                qp.drawPoint(i, j)
        self.drawLabel.setPixmap(pxm)

    def sepiaAction(self):
        self.GSBUTTON = QPushButton(self)
        self.GSBUTTON.setFixedHeight(20)
        self.GSBUTTON.setFixedWidth(90)
        self.GSBUTTON.move(440, 80)
        self.GSBUTTON.setText("Фактор")
        self.GSFACTORINPUT = QLineEdit(self)
        self.GSFACTORINPUT.setFixedHeight(20)
        self.GSFACTORINPUT.setFixedWidth(40)
        self.GSFACTORINPUT.move(380, 80)
        self.GSFACTORINPUT.setValidator(QIntValidator(0, 100, self))
        self.GSBUTTON.clicked.connect(self.sepiaAcTAction)
        self.GSBUTTON.setVisible(True)
        self.GSFACTORINPUT.setVisible(True)

    def bwActualAction(self):
        if self.GSFACTORINPUT.text() == "":
            factor = 1
        else:
            factor = float(self.GSFACTORINPUT.text()) / 100
        if self.GSFACTORINPUT2.text() == "":
            edge = 0
        else:
            edge = int(self.GSFACTORINPUT.text())
        if factor > 1:
            factor = 1
        if factor < 0:
            factor = 1
        self.layout().removeWidget(self.GSFACTORINPUT)
        self.GSFACTORINPUT.deleteLater()
        self.GSFACTORINPUT = None
        self.layout().removeWidget(self.GSFACTORINPUT2)
        self.GSFACTORINPUT2.deleteLater()
        self.GSFACTORINPUT2 = None
        self.layout().removeWidget(self.GSBUTTON)
        self.GSBUTTON.deleteLater()
        self.GSBUTTON = None
        self.layout().removeWidget(self.GSBUTTON2)
        self.GSBUTTON2.deleteLater()
        self.GSBUTTON2 = None
        pxm = self.drawLabel.pixmap()#.copy()
        im  = pxm.toImage()
        a   = pxm.width()
        b   = pxm.height()
        qp  = QPainter(pxm)
        for i in range(a):
            for j in range(b):
                colord = im.pixel(i, j)
                colorm = QColor(colord).getRgb()
                R = colorm[0]
                G = colorm[1]
                B = colorm[2]
                C = int((R + B + G) / 3)
                if C < edge:
                    C = 0
                else:
                    C = 255
                qp.setPen(QPen(QColor(int(C * factor + (1 - factor) * R), int(C * factor + (1 - factor) * G), int(C * factor + (1 - factor) * B)), 1, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
                qp.drawPoint(i, j)
        self.drawLabel.setPixmap(pxm)

    def bwAction(self):
        self.GSBUTTON = QPushButton(self)
        self.GSBUTTON.setFixedHeight(20)
        self.GSBUTTON.setFixedWidth(90)
        self.GSBUTTON.move(440, 80)
        self.GSBUTTON.setText("Фактор")
        self.GSBUTTON2 = QPushButton(self)
        self.GSBUTTON2.setFixedHeight(20)
        self.GSBUTTON2.setFixedWidth(90)
        self.GSBUTTON2.move(440, 120)
        self.GSBUTTON2.setText("Граница")
        self.GSFACTORINPUT = QLineEdit(self)
        self.GSFACTORINPUT2 = QLineEdit(self)
        self.GSFACTORINPUT.setFixedHeight(20)
        self.GSFACTORINPUT.setFixedWidth(40)
        self.GSFACTORINPUT.move(380, 80)
        self.GSFACTORINPUT2.setFixedHeight(20)
        self.GSFACTORINPUT2.setFixedWidth(40)
        self.GSFACTORINPUT2.move(380, 120)
        self.GSFACTORINPUT.setValidator(QIntValidator(0, 100, self))
        self.GSFACTORINPUT2.setValidator(QIntValidator(0, 255, self))
        self.GSBUTTON.clicked.connect(self.bwActualAction)
        self.GSBUTTON.setVisible(True)
        self.GSBUTTON2.setVisible(True)
        self.GSFACTORINPUT.setVisible(True)
        self.GSFACTORINPUT2.setVisible(True)

    def gsActualAct(self):
        if self.GSFACTORINPUT.text() == "":
            factor = 1
        else:
            factor = float(self.GSFACTORINPUT.text()) / 100
        if factor > 1:
            factor = 1
        if factor < 0:
            factor = 1
        self.layout().removeWidget(self.GSFACTORINPUT)
        self.GSFACTORINPUT.deleteLater()
        self.GSFACTORINPUT = None
        self.layout().removeWidget(self.GSBUTTON)
        self.GSBUTTON.deleteLater()
        self.GSBUTTON = None
        pxm = self.drawLabel.pixmap()
        im = pxm.toImage()
        a = pxm.width()
        b = pxm.height()
        qp = QPainter(pxm)
        for i in range(a):
            for j in range(b):
                colord = im.pixel(i, j)
                colorm = QColor(colord).getRgb()
                R = colorm[0]
                G = colorm[1]
                B = colorm[2]
                TR = int((0.393 * R + 0.769 * G + 0.189 * B) * factor + R * (1 - factor))
                if TR > 255:
                    TR = 255
                TG = int((0.349 * R + 0.686 * G + 0.168 * B) * factor + G * (1 - factor))
                if TG > 255:
                    TG = 255
                TB = int((0.272 * R + 0.534 * G + 0.131 * B) * factor + B * (1 - factor))
                if TB > 255:
                    TB = 255
                # print(i, j, TR, TG, TB)
                qp.setPen(QPen(QColor(TR, TG, TB), 1, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
                qp.drawPoint(i, j)
        # print(120)
        self.drawLabel.setPixmap(pxm)
        #self.pixmap = self.drawLabel.pixmap()

    def gsAction(self):
        self.GSBUTTON = QPushButton(self)
        self.GSBUTTON.setFixedHeight(20)
        self.GSBUTTON.setFixedWidth(90)
        self.GSBUTTON.move(440, 80)
        self.GSBUTTON.setText("Фактор")
        self.GSFACTORINPUT = QLineEdit(self)
        self.GSFACTORINPUT.setFixedHeight(20)
        self.GSFACTORINPUT.setFixedWidth(40)
        self.GSFACTORINPUT.move(380, 80)
        self.GSFACTORINPUT.setValidator(QIntValidator(0, 100, self))
        self.GSBUTTON.clicked.connect(self.gsActualAct)
        self.GSBUTTON.setVisible(True)
        self.GSFACTORINPUT.setVisible(True)

    def nsACTAction(self):
        if self.GSFACTORINPUT.text() == "":
            factor = 1
        else:
            factor = float(self.GSFACTORINPUT.text()) / 100
        if self.GSFACTORINPUT2.text() == "":
            edge = 100
        else:
            edge = int(self.GSFACTORINPUT.text())
        if factor > 1:
            factor = 1
        if factor < 0:
            factor = 1
        self.layout().removeWidget(self.GSFACTORINPUT)
        self.GSFACTORINPUT.deleteLater()
        self.GSFACTORINPUT = None
        self.layout().removeWidget(self.GSFACTORINPUT2)
        self.GSFACTORINPUT2.deleteLater()
        self.GSFACTORINPUT2 = None
        self.layout().removeWidget(self.GSBUTTON)
        self.GSBUTTON.deleteLater()
        self.GSBUTTON = None
        self.layout().removeWidget(self.GSBUTTON2)
        self.GSBUTTON2.deleteLater()
        self.GSBUTTON2 = None
        pxm = self.drawLabel.pixmap()#.copy()
        im = pxm.toImage()
        a = pxm.width()
        b = pxm.height()
        qp = QPainter(pxm)
        for i in range(a):
            for j in range(b):
                noise = random.randint(-edge, edge)
                colord = im.pixel(i, j)
                colorm = QColor(colord).getRgb()
                R = colorm[0]
                G = colorm[1]
                B = colorm[2]
                TR = R + noise
                if TR > 255:
                    TR = 255
                if TR < 0:
                    TR = 0
                TG = G + noise
                if TG > 255:
                    TG = 255
                if TG < 0:
                    TG = 0
                TB = B + noise
                if TB > 255:
                    TB = 255
                if TB < 0:
                    TB = 0
                # print(i, j, '{', R, G, B, '}', C)
                qp.setPen(QPen(QColor(int(TR * factor + (1 - factor) * R), int(TG * factor + (1 - factor) * G),
                                      int(TB * factor + (1 - factor) * B)), 1, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
                qp.drawPoint(i, j)
        # print(120)
        # pxm = pxm.fromImage(im)
        self.drawLabel.setPixmap(pxm)
        #self.pixmap = self.drawLabel.pixmap()

    def nsAction(self):
        self.GSBUTTON = QPushButton(self)
        self.GSBUTTON.setFixedHeight(20)
        self.GSBUTTON.setFixedWidth(90)
        self.GSBUTTON.move(440, 80)
        self.GSBUTTON.setText("Фактор")
        self.GSBUTTON2 = QPushButton(self)
        self.GSBUTTON2.setFixedHeight(20)
        self.GSBUTTON2.setFixedWidth(110)
        self.GSBUTTON2.move(440, 120)
        self.GSBUTTON2.setText("Коэфициент")
        self.GSFACTORINPUT = QLineEdit(self)
        self.GSFACTORINPUT2 = QLineEdit(self)
        self.GSFACTORINPUT.setFixedHeight(20)
        self.GSFACTORINPUT.setFixedWidth(40)
        self.GSFACTORINPUT.move(380, 80)
        self.GSFACTORINPUT2.setFixedHeight(20)
        self.GSFACTORINPUT2.setFixedWidth(40)
        self.GSFACTORINPUT2.move(380, 120)
        self.GSFACTORINPUT.setValidator(QIntValidator(0, 100, self))
        self.GSFACTORINPUT2.setValidator(QIntValidator(0, 255, self))
        self.GSBUTTON.clicked.connect(self.nsACTAction)
        self.GSBUTTON.setVisible(True)
        self.GSBUTTON2.setVisible(True)
        self.GSFACTORINPUT.setVisible(True)
        self.GSFACTORINPUT2.setVisible(True)

    def ngActAction(self):
        if self.GSFACTORINPUT.text() == "":
            factor = 1
        else:
            factor = float(self.GSFACTORINPUT.text()) / 100
        if factor > 1:
            factor = 1
        if factor < 0:
            factor = 1
        self.layout().removeWidget(self.GSFACTORINPUT)
        self.GSFACTORINPUT.deleteLater()
        self.GSFACTORINPUT = None
        self.layout().removeWidget(self.GSBUTTON)
        self.GSBUTTON.deleteLater()
        self.GSBUTTON = None
        pxm = self.drawLabel.pixmap()
        im = pxm.toImage()
        a = pxm.width()
        b = pxm.height()
        qp = QPainter(pxm)
        for i in range(a):
            for j in range(b):
                colord = im.pixel(i, j)
                colorm = QColor(colord).getRgb()
                R  = colorm[0]
                G  = colorm[1]
                B  = colorm[2]
                TR = 255 - colorm[0]
                TG = 255 - colorm[1]
                TB = 255 - colorm[2]
                qp.setPen(QPen(QColor(int(TR * factor + (1 - factor) * R), int(TG * factor + (1 - factor) * G), int(TB * factor + (1 - factor) * B)), 1, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
                qp.drawPoint(i, j)
        self.drawLabel.setPixmap(pxm)

    def ngAction(self):
        self.GSBUTTON = QPushButton(self)
        self.GSBUTTON.setFixedHeight(20)
        self.GSBUTTON.setFixedWidth(90)
        self.GSBUTTON.move(440, 80)
        self.GSBUTTON.setText("Фактор")
        self.GSFACTORINPUT = QLineEdit(self)
        self.GSFACTORINPUT.setFixedHeight(20)
        self.GSFACTORINPUT.setFixedWidth(40)
        self.GSFACTORINPUT.move(380, 80)
        self.GSFACTORINPUT.setValidator(QIntValidator(0, 100, self))
        self.GSBUTTON.clicked.connect(self.ngActAction)
        self.GSBUTTON.setVisible(True)
        self.GSFACTORINPUT.setVisible(True)

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

        self.B = [[QLineEdit(self) for i in range(self.m)] for j in range(self.n)]
        
        for i in range(self.n):
            for j in range(self.m):
                self.B[i][j].setFixedWidth(20)
                self.B[i][j].setFixedHeight(20)
                self.B[i][j].move(80 + i * 20, 80 + j * 20)
                self.B[i][j].setValidator(QDoubleValidator(-100, 100, 2))
                self.B[i][j].setVisible(True)
                self.B[i][j].setEnabled(True)
        
        om = self.drawLabel.pixmap()#.copy()
        
        im = om.toImage()
        im.save('burunya_test_drive_ultra.jpg', "JPG")
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
                A[i][j] = float(self.B[i][j].text())
        #print(14)
        image  = Image.open('burunya_test_drive_ultra.jpg')
        im_1   = image.load()
        weight = image.size[0]
        height = image.size[1]
        photo  = Image.new(mode="RGB", size=(int(weight), int(height)))
        draw   = ImageDraw.Draw(photo)
        print(weight, height)
        for k in range(weight):
            for e in range(height):
                for i in range(self.m):
                    for j in range(self.n):
                        #print(k, e, i, j)
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
        photo.save('burunya_test_drive_ultra.jpg', "JPG")
        self.pixmap  = QPixmap('burunya_test_drive_ultra.jpg')
        self.drawLabel.setPixmap(self.pixmap)
        self.drawLabel.resize(self.pixmap.size())
        os.remove('burunya_test_drive_ultra.jpg')
    
    def openImage(self):
        filename = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*);;PNG Files (*.png);;JPG Files (*.jpg)")
        if filename == "":
            return
        self.pixmap  = QPixmap(filename[0])
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
        self.PixMapAv     = True

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
        self.actionFiller.setEnabled(False)
        self.PixMapAv = False

    def exitProg(self):
        self.close()

    def fillEvent(self):
        self.FillClick = True

    def undoAction(self):
        self.actionUndo.setEnabled(False)
        pxm          = QPixmap().fromImage(self.lastpxm)
        self.lastpxm = self.drawLabel.pixmap().toImage()
        self.drawLabel.setPixmap(pxm)
        self.actionRedo.setEnabled(True)

    def redoAction(self):
        self.actionRedo.setEnabled(False)
        pxm          = QPixmap().fromImage(self.lastpxm)
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
            self.drawing   = True
            self.lastPoint = event.pos()
            pxm            = self.drawLabel.pixmap()
            self.lastpxm   = self.drawLabel.pixmap().toImage()
            self.editMenu.setEnabled(True)
            qp  = QPainter(pxm)
            qp.setPen(QPen(self.BrushColor, self.BrushSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            qp.drawPoint(self.lastPoint)
            self.drawLabel.setPixmap(pxm)

        elif event.button() == Qt.LeftButton and self.FillClick:
            self.lastpxm   = self.drawLabel.pixmap().toImage()
            self.editMenu.setEnabled(True)
            self.fillThatShit(event)
            self.FillClick = False

    def doSmth2(self, event):
        if (event.buttons() and Qt.LeftButton) and self.drawing and self.PixMapAv:
            pxm            = self.drawLabel.pixmap()
            self.editMenu.setEnabled(True)
            qp             = QPainter(pxm)
            qp.setPen(QPen(self.BrushColor, self.BrushSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            qp.drawLine(self.lastPoint, event.pos())
            self.lastPoint = event.pos()
            self.drawLabel.setPixmap(pxm)

    def mouseReleaseEvent(self, event):
        if event.button == Qt.LeftButton:
            self.drawing = False

    def fillThatShit(self, event):
        image           = self.drawLabel.pixmap().toImage()
        w, h            = image.width(), image.height()
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