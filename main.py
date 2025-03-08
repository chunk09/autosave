import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QFont
from PyQt5 import uic
import pygetwindow as gw
from src.guide import GuideWindow
import src.save as save

#UI파일 연결
form_class = uic.loadUiType("./widget/main_layout.ui")[0]

#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon('./icon/icon.png'))
        self.setWindowTitle("AutoSave")
        self.setupUi(self)

        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)

        guide_action = QAction('사용법', self)
        guide_action.triggered.connect(self.guide_window) 

        filemenu = menubar.addMenu('도움')
        filemenu.addAction(guide_action)

        # 새로운 위젯 인스턴스를 클래스 속성으로 추가
        self.guide_window_instance = None

        self.second = 1
        self.minute = 0
        self.hour = 0
        self.select_app_name = ""
        self.thread: save.SaveThread = None

        self.sec_bar.valueChanged.connect(self.sec_bar_value)
        self.min_bar.valueChanged.connect(self.min_bar_value)
        self.hour_bar.valueChanged.connect(self.hour_bar_value)

        self.select_app.currentIndexChanged.connect(self.on_combobox_change)

        self.save_btn.clicked.connect(self.on_save)
        self.stop_btn.clicked.connect(self.on_stop)

        self.stop_btn.hide()

        running_windows = gw.getAllWindows()

        self.select_app.addItem("앱 선택")
        
        if running_windows:
            for window in running_windows:
                self.select_app.addItem(window.title)
        else:
            print("No running windows.")

    def guide_window(self):
        if self.guide_window_instance is None:
            self.guide_window_instance = GuideWindow()
        
        self.guide_window_instance.show()
        
    def sec_bar_value(self):
        self.second = self.sec_bar.value()
        self.sec_label.setText("초: " + str(self.second))

    def min_bar_value(self):
        self.minute = self.min_bar.value()
        self.min_label.setText("분: " + str(self.minute))

    def hour_bar_value(self):
        self.hour = self.hour_bar.value()
        self.hour_label.setText("시: " + str(self.hour))
    
    def on_combobox_change(self, index):
        # 콤보 박스에서 선택한 아이템의 이름을 레이블에 표시
        selected_item = self.sender().currentText()
        self.select_app_name = selected_item


    def on_save(self):
        #self.thread.update_signal.connect(self.updateLabel)  # 스레드에서 발생하는 이벤트를 핸들링할 슬롯 연결
        self.thread = save.SaveThread(self.second, self.minute, self.hour, self.select_app_name)
        self.thread.start()

        self.save_btn.hide()
        self.stop_btn.show()

    def on_stop(self):
        self.thread.stop()
        print("스레드 종료")

        self.save_btn.show()
        self.stop_btn.hide()


if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    #WindowClass의 인스턴스 생성
    myWindow = WindowClass() 

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()