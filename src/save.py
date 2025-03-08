import time
from PyQt5.QtCore import QThread
import pyautogui
import pygetwindow
import keyboard

class SaveThread(QThread):
    def __init__(self, sec: int, min: int, hour: int, app_name: str):
        super().__init__()
        self.sec = sec
        self.min = min
        self.hour = hour
        self.app_name = app_name

        self.target_window = self.get_target_window()

        self.time_saveable = False
        self.typing_saveable = False

        self.timer = 0
        self.typing_timer = 0

    def run(self):
        min_to_sec = self.min * 60 # 분을 초 단위로
        hour_to_sec = self.hour * 3600 # 시를 초 단위로

        select_time = self.sec + min_to_sec + hour_to_sec

        while not self.isInterruptionRequested():
            # 1초마다 타이머 1씩 올라감
            self.timer += 1
            self.typing_timer += 1

            self.typing_saveable = False
            keyboard.hook(self.on_any_key_event) # 타이핑 감지

            if self.timer == select_time: # 타이머가 지정한 시간과 시간이 똑같아 질 때
                print(str(select_time) + "초가 되었습니다.")
                self.time_saveable = True

                self.timer = 0 # 타이머 초기화

            if self.typing_timer == 3: # 사용자가 3초 동안 타이핑 안했을 때
                print("사용자가 3초 동안 키보드를 타이핑하지 않았습니다.")
                self.typing_saveable = True
                self.typing_timer = 0 # 키보드 타이머 초기화

            if self.time_saveable and self.typing_saveable: # 지정된 시간이 됐고 키보드 타이핑을 3초 이상 안했을 때
                # 현재 윈도우
                current_window = pygetwindow.getActiveWindow() 

                # 지정한 윈도우와 현재 윈도우가 같은 지 확인
                if current_window in self.target_window:
                    # 현재 윈도우와 지정한 윈도우가 같다면

                    pyautogui.hotkey("ctrl", "s") # 저장

                    self.time_saveable = False
                    self.typing_saveable = False  

                    print("저장 됨")
                else:
                    print("현재 사용 중인 윈도우는 사용자가 지정한 윈도우가 아닙니다.")

            # time.sleep(1)
            self.msleep(1000)

    def on_any_key_event(self, e):                                                     
        self.typing_timer = 0 # 키를 누를 때 타이머 초기화


    def stop(self):
        self.requestInterruption()
        self.wait()  # 스레드가 완전히 종료될 때까지 대기합니다.

        print("종료")


    def get_target_window(self) -> list:
        try:
            windows = pygetwindow.getAllWindows()
            
            for window in windows:
                win_title: str = window.title

                if self.app_name in win_title:
                    target_window = pygetwindow.getWindowsWithTitle(win_title)

                    return target_window
                
        except Exception as e:
            print("에러 발생: ", e)
