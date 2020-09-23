import sys
from os import walk
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QAction, QFileDialog, QLabel, QVBoxLayout, QPushButton, QWidget, QMessageBox
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
        if idx>0:
            self.target = idx-1
        else:
            pass
        self.showImg()


    def handleNextBtn(self):
        idx = self.target
        work_files = self.work_files

        if idx<len(work_files)-1:
            self.target = idx+1
        else:
            pass

        self.showImg()
      
    def handleSaveBtn(self):
        import shutil, os
        emotions = self.emotions
        for filename in emotions:
            emotion = emotions[filename]
            # 경로 존재하는지 확인
            if not os.path.isdir(self.work_dir + '/' + emotion):
                os.mkdir(self.work_dir + '/' + emotion)
            prev_path = self.work_dir + '/' + filename
            new_path = self.work_dir + '/' + emotion + '/' + filename
            # print(prev_path,new_path)
            shutil.move(prev_path, new_path)
        self.initUI()


    def setWorkDir(self):
        work_dir = self.work_dir
        f = []
        for (_, _, filenames) in walk(work_dir):
            f.extend(filenames)
            break

        f.sort()
        self.work_files = f
        self.target = 0
        self.emotions = dict()


    def setButtons(self):
        prev_btn = QPushButton('prev', self)
        prev_btn.clicked.connect(self.handlePrevBtn)
        next_btn = QPushButton('next', self)
        next_btn.clicked.connect(self.handleNextBtn)
        save_btn = QPushButton('save', self)
        save_btn.clicked.connect(self.handleSaveBtn)


        self.layout.addWidget(prev_btn)
        self.layout.addWidget(next_btn)
        self.layout.addWidget(save_btn)


    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()
        elif e.key() == Qt.Key_Q:
            # happy
            self.emotions[self.work_files[self.target]] = 'happy'
            self.showImg()
        elif e.key() == Qt.Key_W:
            # sad
            self.emotions[self.work_files[self.target]] = 'sad'
            self.showImg()
        elif e.key() == Qt.Key_E:
            # else
            self.emotions[self.work_files[self.target]] = 'else'
            self.showImg()
        elif e.key() == Qt.Key_D:
            # delete label
            del self.emotions[self.work_files[self.target]]
            print(self.emotions)
            self.showImg()
        elif e.key() == Qt.Key_Right:
            self.handleNextBtn()
        elif e.key() == Qt.Key_Left:
            self.handlePrevBtn()

    def showImg(self):
        print(self.work_dir+'/'+self.work_files[self.target])
        pixmap = QPixmap(self.work_dir+'/'+self.work_files[self.target])

        lbl_img = QLabel()
        lbl_img.setPixmap(pixmap)
        lbl_img.setAlignment(Qt.AlignCenter)
        filename = self.work_files[self.target]
        emotion = self.emotions[filename] if filename in self.emotions else ''
        lbl_info = QLabel(filename+'\n'+emotion)
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