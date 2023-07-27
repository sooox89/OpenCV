import cv2
import threading
import sys
import time
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore

running = False

# 동영상 파일 경로 (동영상 파일 열 경우)
video_path = "/Users/sooox89/Desktop/workspace/pythonProject/computervision/team3/yolo_test/sample_960x400_ocean_with_audio.mp4"

def run():
    global running
    # 카메라 또는 동영상 열기
    cap = cv2.VideoCapture(0)   # 카메라 index는 조정하세요!
    # cap = cv2.VideoCapture(video_path)  # 동영상 파일 열기

    # 원본 동영상 크기 정보
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

    # 동영상 크기 변환P
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # 가로
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # 세로
    # 변환된 동영상 크기 정보
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

    label.resize(int(width), int(height))

    FPS = cap.get(cv2.CAP_PROP_FPS)
    delay = round(1000/FPS)

    while running:
        ret, img = cap.read()


        if ret:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            h,w,c = img.shape
            qImg = QtGui.QImage(img.data, w, h, w*c, QtGui.QImage.Format_RGB888)
            pixmap = QtGui.QPixmap.fromImage(qImg)
            label.setPixmap(pixmap)

            if cv2.waitKey(delay) == 27:
                break


        else:
            QtWidgets.QMessageBox.about(win, "Error", "Cannot read frame.")
            print("cannot read frame.")
            break
    cap.release()   # 동영상 파일 , 카메라 닫고 메모리 해제

    print("Thread end.")

def stop():
    global running
    running = False
    print("stoped..")
    cv2.destroyAllWindows()

def start():
    global running
    running = True
    th = threading.Thread(target=run)
    th.start()
    print("started..")


def onExit():
    print("exit")
    stop()

app = QtWidgets.QApplication([])
win = QtWidgets.QWidget()
vbox = QtWidgets.QVBoxLayout()
label = QtWidgets.QLabel()
btn_start = QtWidgets.QPushButton("Camera On")
btn_stop = QtWidgets.QPushButton("Camera Off")
vbox.addWidget(label)
vbox.addWidget(btn_start)
vbox.addWidget(btn_stop)
win.setLayout(vbox)
win.show()

btn_start.clicked.connect(start)
btn_stop.clicked.connect(stop)
app.aboutToQuit.connect(onExit)

sys.exit(app.exec_())