from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QPushButton, QTextEdit
import csv  # CSV 파일 저장을 위해 추가

Form, Window = uic.loadUiType("res/mainWin.ui")

def on_button_click():
    # 텍스트 입력 위젯에서 정보를 가져와 CSV 파일에 저장
    text_edit = window.findChild(QTextEdit, "textEditName")  # "textEditName"을 UI에 정의된 QTextEdit 이름으로 변경
    if text_edit:
        content = text_edit.toPlainText()
        if content.strip():  # 내용이 비어있지 않은 경우에만 저장
            with open("data.csv", "a", encoding="utf-8", newline="") as file:  # 파일명을 data.csv로 변경
                writer = csv.writer(file)
                writer.writerow([content])  # 한 줄씩 저장
            print("Content saved to data.csv")
        else:
            print("No content to save.")
    else:
        print("Error: TextEdit with objectName 'textEditName' not found in the UI.")

app = QApplication([])
window = Window()
form = Form()
form.setupUi(window)

# 버튼 객체를 가져와 클릭 이벤트 연결
button = window.findChild(QPushButton, "buttonName")  # "buttonName"을 UI에 정의된 버튼 이름으로 변경
if button:
    button.clicked.connect(on_button_click)
    print("Button connected successfully.")
else:
    print("Error: Button with objectName 'buttonName' not found in the UI.")

window.show()
app.exec()
