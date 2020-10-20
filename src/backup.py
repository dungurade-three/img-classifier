import sys
from os import walk
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QAction, QFileDialog, QLabel, QVBoxLayout, QPushButton, QWidget
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
# from PyQt5.QtWidgets import QApplication, , QPushButton, QHBoxLayout, QVBoxLayout, 

class MyApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        widget = QWidget()
        layout = QVBoxLayout(widget)
        self.layout = layout
        self.setCentralWidget(widget)

        self.statusBar()
        openFile = QAction(QIcon('open.png'), 'Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open New File')
        openFile.triggered.connect(self.showDialog)

        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)        

        self.setWindowTitle('Box Layout')
        self.setGeometry(500, 500, 700, 700)
        self.show()


    def showDialog(self):
        work_dir = QFileDialog.getExistingDirectory(self, 'work dir', '/')
        if work_dir:
            self.work_dir = work_dir
            print(work_dir)
            self.setWorkDir()
            self.setButtons()
            self.showImg()

    def handlePrevBtn(self):
        idx = self.target
        work_files = self.work_files

        if idx>0:
            self.target = idx-1
        else:
            self.target = len(work_files)-1
        self.showImg()


    def handleNextBtn(self):
        print('handleNextBtn')
        idx = self.target
        work_files = self.work_files

        if idx<len(work_files)-1:
            self.target = idx+1
        else:
            self.target = 0
        self.showImg()


    def setWorkDir(self):
        work_dir = self.work_dir
        f = []
        for (_, _, filenames) in walk(work_dir):
            f.extend(filenames)
            break

        f.sort()
        self.work_files = f
        self.target = 0


    def setButtons(self):
        prev_btn = QPushButton('prev', self)
        next_btn = QPushButton('next', self)
        next_btn.clicked.connect(self.handleNextBtn)

        self.layout.addWidget(prev_btn)
        self.layout.addWidget(next_btn)


    def showImg(self):
        print(self.work_dir+'/'+self.work_files[self.target])
        pixmap = QPixmap(self.work_dir+'/'+self.work_files[self.target])

        lbl_img = QLabel()
        lbl_img.setPixmap(pixmap)
        lbl_img.setAlignment(Qt.AlignCenter)
        lbl_info = QLabel(self.work_files[self.target])
        lbl_info.setAlignment(Qt.AlignCenter)
        
        if hasattr(self, 'lbl_img'):
            self.layout.takeAt(self.layout.indexOf(self.lbl_img)).widget().deleteLater()
            self.layout.addWidget(lbl_img)
            self.layout.takeAt(self.layout.indexOf(self.lbl_info)).widget().deleteLater()
            self.layout.addWidget(lbl_info)
        else:
            self.layout.addWidget(lbl_img)
            self.layout.addWidget(lbl_info)

        self.lbl_img = lbl_img
        self.lbl_info = lbl_info
        self.layout.update()

def start():
        app = QApplication(sys.argv)
        ex = MyApp()
        sys.exit(app.exec_())

if __name__ == "__main__":
    start()