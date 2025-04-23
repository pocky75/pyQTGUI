from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QPushButton, QLineEdit, QTextEdit, QLabel, QMessageBox
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import QTimer
import cv2
import csv
import os

Form, Window = uic.loadUiType("res/mainWin.ui")

# OpenCV 관련 설정
cap = cv2.VideoCapture(0)  # 웹캠 열기
captured_image = None  # 캡처된 이미지를 저장할 변수

def update_webcam():
    ret, frame = cap.read()
    if ret:
        # 프레임 크기 조정
        resized_frame = cv2.resize(frame, (160, 120))  # QLabel 크기에 맞게 조정
        frame_rgb = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
        h, w, ch = frame_rgb.shape
        bytes_per_line = ch * w
        qimg = QImage(frame_rgb.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(qimg)
        webcam_label = window.findChild(QLabel, "label_wepcam")  # 웹캠 영상을 표시할 QLabel
        if webcam_label:
            webcam_label.setPixmap(pixmap)

def show_message(title, message):
    """알림 메시지를 표시하는 함수"""
    msg_box = QMessageBox()
    msg_box.setWindowTitle(title)
    msg_box.setText(message)
    msg_box.exec()

def on_capture_button_click():
    global captured_image
    ret, frame = cap.read()
    if ret:
        captured_image = frame  # 캡처된 이미지를 저장
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = frame_rgb.shape
        bytes_per_line = ch * w
        qimg = QImage(frame_rgb.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(qimg)
        photo_label = window.findChild(QLabel, "label_photo")  # 캡처된 이미지를 표시할 QLabel
        if photo_label:
            photo_label.setPixmap(pixmap)

        # 이름 입력란에서 이름 가져오기
        name_input = window.findChild(QLineEdit, "lineEdit_name")
        if name_input:
            name = name_input.text().strip()
            if name:
                # photo 폴더 생성
                os.makedirs("photo", exist_ok=True)
                image_path = os.path.join("photo", f"{name}.jpg")
                cv2.imwrite(image_path, captured_image)
                print(f"이미지가 {image_path}에 저장되었습니다.")
                show_message("촬영 완료", f"이미지가 {name}.jpg로 저장되었습니다.")
            else:
                show_message("촬영 실패", "이름을 입력하세요.")
        else:
            print("Error: QLineEdit with objectName 'lineEdit_name' not found in the UI.")
    else:
        print("웹캠에서 이미지를 캡처할 수 없습니다.")

def on_save_button_click():
    global captured_image
    # 입력 필드에서 정보 가져오기
    name = window.findChild(QLineEdit, "lineEdit_name").text().strip()
    phone = window.findChild(QLineEdit, "lineEdit_phonenumber").text().strip()
    memo = window.findChild(QTextEdit, "textEdit_recommand").toPlainText().strip()

    # 정보가 입력되었는지 확인 후 저장
    if name and phone:
        # CSV 파일에 정보 저장
        with open("data.csv", "a", encoding="utf-8", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([name, phone, memo])
        print("정보가 저장되었습니다.")

        # 캡처된 이미지 저장
        if captured_image is not None:
            # photo 폴더 생성
            os.makedirs("photo", exist_ok=True)
            image_path = os.path.join("photo", f"{name}.jpg")
            cv2.imwrite(image_path, captured_image)
            print(f"이미지가 {image_path}에 저장되었습니다.")
            show_message("저장 완료", f"정보와 이미지가 {name}.jpg로 저장되었습니다.")
        else:
            print("캡처된 이미지가 없습니다. 촬영 버튼을 눌러 이미지를 캡처하세요.")
            show_message("저장 실패", "캡처된 이미지가 없습니다. 촬영 버튼을 눌러 이미지를 캡처하세요.")
    else:
        print("이름과 전화번호는 필수 입력 항목입니다.")
        show_message("저장 실패", "이름과 전화번호는 필수 입력 항목입니다.")

app = QApplication([])
window = Window()
form = Form()
form.setupUi(window)

# QTimer를 사용하여 웹캠 프레임 업데이트
timer = QTimer()
timer.timeout.connect(update_webcam)
timer.start(30)  # 30ms마다 프레임 업데이트

# 저장 버튼 객체를 가져와 클릭 이벤트 연결
save_button = window.findChild(QPushButton, "btnSave")  # "btnSave"는 UI 파일에서 저장 버튼의 objectName
if save_button:
    save_button.clicked.connect(on_save_button_click)
else:
    print("Error: QPushButton with objectName 'btnSave' not found in the UI.")

# 촬영 버튼 객체를 가져와 클릭 이벤트 연결
capture_button = window.findChild(QPushButton, "camera")  # "camera"는 UI 파일에서 촬영 버튼의 objectName
if capture_button:
    capture_button.clicked.connect(on_capture_button_click)
else:
    print("Error: QPushButton with objectName 'camera' not found in the UI.")

window.show()
app.exec()

# 프로그램 종료 시 웹캠 해제
cap.release()