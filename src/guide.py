from PyQt5.QtWidgets import QWidget
from PyQt5 import uic
from PyQt5.QtGui import QIcon, QFont

#UI파일 연결
form_class = uic.loadUiType("./widget/guide.ui")[0]

class GuideWindow(QWidget, form_class):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon('./icon/icon.png'))
        self.setWindowTitle("사용법")
        self.setupUi(self)